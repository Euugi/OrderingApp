function countCartValue() {

    let elements = [];

    $("button[id^='btn-add-']").each(function(){
    elements.push(this.id); 
    });
    console.log(elements);
    let cart_value = $('#cart-value').text();
    console.log("before " + cart_value);
    for (let i = 0; i < elements.length; i++) {
        if(document.getElementById(elements[i]).clicked == true)
        {
            console.log("clicked")
            price = Integer.parseInt($('price-' + i).val());
            cart_value = Integer.parseInt(cart_value);
            cart_value += price;
            $('#cart-value').text(cart_value);
            console.log("after " + cart_value);
        }
    }
}

    $(document).ready(function () {
        console.log("test")
        $("button[name='order-button']").click(function() {
          checked = $("input[type=checkbox]:checked").length;
    
          if(!checked) {
            alert("Musisz wybrać conajmniej jedno danie aby złożyć zamówienie.");
            return false;
          }

          if (document.getElementById("delivery_address").value == '') {
              alert("Adres dostawy nie może być pusty")
              return false;
          }
    
        });
    });


    /*let cart_value = $('#cart-value').text();
    window.onload = myMain;

    function myMain() {
        document.getElementById("dishes-table").onclick = checkButton;
    }
      
    function checkButton(e) {
        if (e.target.tagName == 'BUTTON') {
            let id = e.target.id;
            let price = $("#price-" + id).text();
            if ($('#cart-value').text() == '') {
                $('#cart-value').text(price);
            }
            else {
                let current_value = $('#cart-value').text();
                current_value = parseFloat(current_value);
                current_value += parseFloat(price);
                Number((current_value).toFixed(2));
                $('#cart-value').text(current_value);
            }
        }
    }
    //countCartValue();
*/