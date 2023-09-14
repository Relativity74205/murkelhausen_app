// form_focus.js
function setFocusOnField(fieldId) {
    document.addEventListener("DOMContentLoaded", function() {
        var inputField = document.getElementById(fieldId);
        if (inputField) {
            inputField.focus();
        }
    });
}