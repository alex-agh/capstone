// Initialize Monaco Editor inside the container element

function initEditor() {
    require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.28.0/min/vs' }});
    return new Promise((resolve, reject) => {
        require(['vs/editor/editor.main'], function() {
            // Customize the editor options
            var editor = monaco.editor.create(document.getElementById('editorContainer'), {
                value: '',
                language: 'csharp',
                theme: 'vs-dark',
                fontSize: 16
            });

            // Resolve the promise with the editor object
            resolve(editor);
        });
    });
}
    
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

document.getElementById('executeButton').addEventListener('click', function() {
    // Get the code from the editor
    var code = editor.getValue();

    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/dashboard/run-code/',
        method: 'POST',
        data: {
            code: code,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(response) {
            console.log(response.output);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });

    // Execute the code and get the output
    var output = executeCode(code);
    
    // Display the output in a dialog or on the page
    // alert(output);
});

function executeCode(code) {
    // Executable code goes here!

    return "Hello World!"
}  




