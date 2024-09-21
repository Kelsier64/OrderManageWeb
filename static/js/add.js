document.getElementById('platform-select').addEventListener('change', function() {
    var trs = document.querySelectorAll('.trs');
    trs.forEach(function(tr) {
        tr.classList.add('hidden');
    });
    if(this.value === "all"){
        trs.forEach(function(tr) {
            tr.classList.remove('hidden');
        });     
    }else{
        var selectedCategory = document.querySelectorAll("."+this.value);
        selectedCategory.forEach(function(tr) {
            tr.classList.remove('hidden');
        });
    }
    
});

function increment(button) {
    var input = button.parentNode.parentNode.querySelector('input[type="number"]');
    if (input.value >= 0) {
        input.value = parseInt(input.value) + 1;
    }else{
        input.value = 0;
    }
}

function decrement(button) {
    var input = button.parentNode.parentNode.querySelector('input[type="number"]');
    if (input.value > 0) {
        input.value = parseInt(input.value) - 1;
    }else{
        input.value = 0;
    }
}