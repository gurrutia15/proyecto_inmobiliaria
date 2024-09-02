function filtrar_comunas () {
    // Obtener cod de la región
    const region_id = $(this).val()
    // Iteramos sobre todas las comunas y mostramos sólo aquellas cuyo prefijo tenga el region_id
    $('#comuna_id').val('')
    $('#comuna_id option').each(function(){
        const comuna= $(this)
        const comuna_region_id = comuna.data('region-id')
        if (region_id == comuna_region_id){
            comuna.show()
        } else {
            comuna.hide()
        }
    })
}

// Ejecuta la función filtrar_comuna al detectar cambios
$('#region_id').on('change', filtrar_comunas)