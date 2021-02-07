$(document).ready(function(){
    $('#form-start-validate').submit(function(){
        let user_name = $('#form-start-validate input#user_name').val()
        if(user_name == ""){
            alert('Informe seu nome por favor!');
            return false;
        }
    });
    $('#form-word-intrusion').submit(function(){
        let quantityTopics = $('.topic-line').length;
        let quantityRadioChecked = $("input:checked").length;
        if (quantityRadioChecked != quantityTopics){
            alert('Por favor, selecione ao menos uma palavra de cada tópico')
            return false;
        }
    });

    $('#form-topic-intrusion').submit(function(){

        let quantityDocs = $('.doc-card').length;
        let quantityRadioChecked = $("input:checked").length;
        if (quantityRadioChecked != quantityDocs){
            alert('Por favor, selecione ao menos uma lista palavra de cada documento')
            return false;
        }
    });

});