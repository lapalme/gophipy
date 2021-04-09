$(document).ready(function() {
    $.getJSON("../gophi-web/lexicon-dme.json", function(lexiconDME){
        addLexiconEn(lexiconDME);
        setReorderVPcomplements(true);
        resetSavedWarnings();
        let sent=null;
        try {
            sent=eval(syntR).toString(); // generate sentence by evaluating the generated expression
            // console.log(sent)
            sent=sent.replace(/\[\[(.*?)\]\]/g,'$1'); // clean unknown word flags
            $("#realization").html(sent)
            const jsRealWarnings=getSavedWarnings();
            if (jsRealWarnings.length>0){
                $("#realization").append(`
                    <h3>Realization warnings</h3>
                    <p>${jsRealWarnings.join("<br/>")}</p>`)
            }
        } catch (err) {
            $("#realization").html(`
                <h3>Error in syntactic representation</h3>
                <b>${err.name}</b>: ${err.message}`)
        }
    })
});
