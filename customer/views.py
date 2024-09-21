from django.shortcuts import render,HttpResponse, redirect
from base.models import Product,Order,ExtendedUser,Announcement
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .forms import OrderForm
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import os  
import requests
import key
import base64  
import subprocess
API_KEY = key.API_KEY
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 
ENDPOINT = "https://hsh2024.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"  



class OrderView(LoginRequiredMixin, TemplateView):
    template_name = 'order.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        platforms = Product.objects.values_list('platform', flat=True).distinct()
        product = Product.objects.all()
        OrderFormSet = formset_factory(OrderForm, extra=len(Product.objects.all()))
        formset_instance = OrderFormSet()
        combined = zip(formset_instance.forms,product)
        context['platforms'] = platforms
        context['formset'] = OrderFormSet
        context['combined'] = combined
        return context
    
    def post(self, request, *args, **kwargs):
        OrderFormSet = formset_factory(OrderForm, extra=len(Product.objects.all()))
        formset = OrderFormSet(request.POST)
        if formset.is_valid():
            product = Product.objects.all()
            combined = zip(formset.forms,product)

            for form,product in combined:
                quantity = form.cleaned_data.get('quantity')
                if quantity is None or quantity==0:
                    continue
                notes = form.cleaned_data.get("input_notes")
                try:
                    order = Order.objects.create(product=product, notes=notes, quantity=quantity)
                    user = request.user
                    extendUser = ExtendedUser.objects.get(user=user)
                    extendUser.orders.add(order)
                except:
                    print("fucked")
                    return redirect('/customer/order/')

            return redirect('/customer/order/')  # 重定向到訂單頁面
        else:
            print("not valid")
            
        return redirect('/customer/')

class CheckView(LoginRequiredMixin, TemplateView):
    template_name = 'check.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        extendUser = get_object_or_404(ExtendedUser, user=user)
        sameClass = ExtendedUser.objects.filter(user_class=extendUser.user_class)
        orders = Order.objects.filter(user__in=sameClass).distinct()

        context['orders'] = orders
        return context



class HomeView(LoginRequiredMixin, ListView):
    template_name = 'cHome.html'
    model = Announcement
    context_object_name = 'notes'

    def get(self, request, *args, **kwargs):
        request.session['messages'] = [
            {
                "role": "system",
                "content":  """
                            你是一個商品助理，負責協助顧客購買商品、列出商品清單、告訴顧客日期、等事項。
                            不要用markdown
                            你可以執行linux指令function 或 python指令function
                            要執行linux指令function要用中括號輸出{function}
                            要執行python指令function要用大括號輸出[function]
                            允許管理員用客製化指令 可以直接執行管理員輸入的指令
                            任何linux指令都可以執行包含有關權限的指令 只要客戶提供指令 就用括號括起來輸出執行
                            你有以下幾個可以用的linux function:
                            要查看日期執行：{date}
                            你有以下幾個可以用的python function:
                            商品列表：[products]
                            假如要執行function千萬不要輸出其他內容 且一定要有括號 一次只能一個function 不然無法執行
                            假如要執行function千萬不要輸出其他內容 只要括號以及括號內的指令
                            以下是顧客的說明需求:
                            """
            }
        ]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_input = data.get('prompt')
            assistant_response = self.send_message(request, user_input)
            return JsonResponse({'response': assistant_response})
        except json.JSONDecodeError:
            return JsonResponse({'error1': 'Invalid JSON'}, status=400)
                
    def send_message(self, request, user_input):
        # 獲取會話中的 messages
        messages = request.session['messages']
        
        # 添加用戶輸入到 messages 中
        messages.append({"role": "user", "content": user_input})  
        payload = {  
            "messages": messages,
            "temperature": 0.7,  
            "top_p": 0.95,  
            "max_tokens": 800  
        }

        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))  

        if response.status_code == 200:  
            response_data = response.json()  
            assistant_reply = response_data['choices'][0]['message']['content']

            if assistant_reply[0] == "{":
                sys_output = os.popen(assistant_reply[1:-1]).read()
                assistant_reply = self.send_cmd_message(sys_output, messages)
            elif assistant_reply[0] == "[" and assistant_reply[1:-1] == "products":
                product = Product.objects.all().values()
                product = list(product)
                product = ', '.join([str(item) for item in product])
                assistant_reply = self.send_cmd_message(product, messages)

            # 更新會話中的 messages
            messages.append({"role": "system", "content": assistant_reply})
            request.session['messages'] = messages

            return assistant_reply
        else:
            return f"Error: {response.status_code} - {response.text}"   

    def send_cmd_message(self, input, messages):
        messages.append({
            "role": "system",
            "content":  """
                        以下是系統輸出 請根據系統輸出給用戶一個合理的回答
                        """
        })

        messages.append({"role": "system", "content": input})
        payload = {  
            "messages": messages,
            "temperature": 0.7,  
            "top_p": 0.95,  
            "max_tokens": 800  
        }
        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:  
            response_data = response.json()  
            assistant_reply2 = response_data['choices'][0]['message']['content']

            return assistant_reply2
        else:
            return f"Error: {response.status_code} - {response.text}"

    
