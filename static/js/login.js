jQuery(window).load(function() {
    //Após a leitura da pagina o evento fadeOut do loader é acionado, esta com delay para ser perceptivo em ambiente fora do servidor.
    jQuery("#loader").delay(2000).fadeOut("slow");
});