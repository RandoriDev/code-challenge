function submit_json( form ){
    // Encodes the visible form data into a JSON string.
    form_json = to_json_string(form);
    // Storing the JSON-encoded string in a hidden element which will then be submitted.
    document.getElementById("json_element").value = form_json;
    document.getElementById("hidden_form").submit();
}

function to_json_string( form ) {
    // Encodes form data into a JSON string.
    var object = {};
    var form_elements = form.querySelectorAll( "input, select, textarea" );
    for( var i = 0; i < form_elements.length; ++i ) {
        var form_element = form_elements[i];
        var name = form_element.name;
        var value = form_element.value;

        // Check if is_malicious is checked.
        if( name == 'is_malicious' && form_element.checked == true ){
            object[ name ] = 'is_malicious';
        }
        // If is_malicious is not checked, give it an empty value.
        else if ( name == 'is_malicious' ){
            object[ name ] = '';
        }
        // Handle every other element.
        else if ( name ) {
            object[ name ] = value;
        }
    }

    return JSON.stringify( object );
}
