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




