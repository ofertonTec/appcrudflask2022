cantidad = 0

function escucharInput(event) {
    cantidad = event.srcElement.value
    console.log('valor: ' + cantidad);
}
codsProductosSeleccionados = []
listaProductos = []

//INICIO: Guardar productos al localstorage
function agregarCarrito(event, codigo, nombre, precio_lista, foto) {
    event.preventDefault()
    if (localStorage.getItem('productosSeleccionados') == null) {
        localStorage.setItem('productosSeleccionados', '');
    }
    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio_lista,
        "foto": foto
    }

    existe=[]
    for(prod in listaProductos){
        if(listaProductos[prod].codigo == codigo){
            existe.push(true)
        }
    }
    console.log(existe)
    if(existe.length==0){
        listaProductos.push(producto)
        Swal.fire(
            'Exitoso!',
            'Producto agregado exitosamente',
            'success'
        );
        document.getElementById("cantidadTotal").value = "";
    }else{
       existe=[]
       Swal.fire(
        'Hey!',
        'Ya agregaste el producto',
        'warning'
    );
    }
    //localStorage.setItem('listaProductos',JSON.stringify(listaProductos));
    mostrarListProductSelect(listaProductos)
}
//FIN: Guardar productos al localstorage




function mostrarListProductSelect(data) {
    $('#conteneror_List_items').remove()
    //INICIO: contendor padreForm
    contenedor_form = document.getElementById('contenedorForm')
    contenedor_form.classList.add('modal-body')
    conteneror_List_items = document.createElement('div')
    conteneror_List_items.id = 'conteneror_List_items'
    contenedor_form.appendChild(conteneror_List_items)
    //FIN: contendor padreForm

    for (i = 0; i < data.length; i++) {     
            var codigo = data[i].codigo
            var nombre = data[i].nombre
            var precio = data[i].precio
            var cantidad = data[i].cantidad
            var total = data[i].total
            var foto = data[i].foto

            contenedor_items = document.createElement('div')
            contenedor_items.id = 'contenedor_items'


            //Creando los div item
            items = document.createElement('div')
            items.id = 'items_list'
            items.classList.add('row', 'text-center', 'align-items-center', 'border-bottom', 'border-dark', 'mb-3')

            //Creando  div imagen
            item_imagen = document.createElement('div')
            item_imagen.classList.add('col', 'p-1')
            //<img id="imagen_" width="150px" class="img-thumbnail" src="/uploads/2022093624IAUNTSN6SZA37BPTWR4AZBPZUM.jpg" >
            img_ = document.createElement('img')
            img_.classList.add('img-thumbnail')
            img_.width = 150
            img_.src = '/uploads/' + foto

            item_imagen.appendChild(img_)
            //Creando  div precio
            item_precio = document.createElement('div')
            item_precio.classList.add('col', 'p-1')
            precio_ = document.createTextNode(precio)
            item_precio.appendChild(precio_)

            //Creando  div cantidad
            item_cantidad = document.createElement('div')
            item_cantidad.classList.add('col', 'p-1')
            cantidad_ = document.createTextNode(cantidad)
            item_cantidad.appendChild(cantidad_)

            //Creando  total
            item_total = document.createElement('div')
            item_total.classList.add('col', 'p-1')
            nombre_ = document.createTextNode(nombre)
            item_total.appendChild(nombre_)

            //Creando  div button
            item_button = document.createElement('div')
            item_button.classList.add('col', 'p-1')
            // <button id="eliminar_item" class="btn  btn-light"> <i class="fa-solid fa-trash"> </i> </button>
            eliminar_item = document.createElement('button')
            eliminar_item.classList.add('btn', 'btn-light')

            //
            eliminar_item.innerHTML = "Eliminar";
            eliminar_item.onclick = function(event) {
                event.preventDefault()
                eliminarItem(codigo)
            };
            //
            // icon
            icono = document.createElement('i')
            icono.classList.add('fa-solid', 'fa-trash')

            item_button.appendChild(eliminar_item)
            item_button.id="item/"+codigo
            
            eliminar_item.appendChild(icono)

            //ORDENANDO LOS VALORES
            items.appendChild(item_imagen)
            items.appendChild(item_precio)
            items.appendChild(item_cantidad)
            items.appendChild(item_total)
            items.appendChild(item_button)
            contenedor_items.appendChild(items)
            conteneror_List_items.appendChild(contenedor_items)
        
    }
}
function eliminarItem(codigo){
    alert('Selecciono el elemento con codigo: ' + codigo)

}
/*function agregarCarrito(event, codigo, nombre, precio_lista, foto) {
    event.preventDefault()
    codsProductosSeleccionados.push(codigo)
    localStorage.setItem("Codigos", JSON.stringify(codsProductosSeleccionados))
    console.log(productoExiste(codigo))
    if (productoExiste(codigo)) {
        total = parseFloat(cantidad) * parseFloat(precio_lista)
        $.ajax({
            url: '/btnAgreagarCarrito',
            type: 'GET',
            data: {
                codigo: codigo,
                nombre: nombre,
                cantidad: cantidad,
                precio: precio_lista,
                total: total,
                foto: foto

            },
            success: function (response) {
                mostrarData(response)
                console.log(typeof response)
            },
            error: function (response) {
                console.log('Error')
            }
        })
    } else {
        alert('Ya ingreso el producto')
    }


}*/
