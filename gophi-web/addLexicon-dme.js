function addLexiconEn(dmeLexicon){
    // console.log("addLexiconEn");
    loadEn(false); // make sure additions are to the English lexicon

    updateLexicon(dmeLexicon);
    // console.log("after update lexicon",Object.keys(getLexicon()).length)
    // ajouts au lexique de JSrealB (version dme)
    addToLexicon("tsunami",{"N":{"tab":["n1"]}});
    addToLexicon("sushi",{"N":{"tab":["n1"]}});

    ////////////////// Additions for SRST 2019

    // modern words 
    addToLexicon({"download":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}}) //  load
    addToLexicon({"upload":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}})   //  load
    addToLexicon({"email":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}})    //  mail
    addToLexicon({"e-mail":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}})   //  mail
    addToLexicon({"ecommerce":{"N":{"tab":["n5"]}}})                 // commerce
    addToLexicon({"e-commerce":{"N":{"tab":["n5"]}}})
    addToLexicon({"database":{"N":{"tab":["n1"]}}})                // base Noun       
    addToLexicon({"data-base":{"N":{"tab":["n1"]}}})               // base Noun
    addToLexicon({"browser":{"N":{"tab":["n1"]}}})                 // dowser
    addToLexicon({"online":{"N":{"tab":["n1"]}}})                  // airline
    addToLexicon({"fax":{"N":{"tab":["n2"]},"V":{"tab":"v2"}}})    // tax
    addToLexicon({"smartphone":{"N":{"tab":["n1"]}}})              // gramophone
    addToLexicon({"iphone":{"N":{"tab":["n1"]}}})                  // gramophone
    addToLexicon({"spreadsheet":{"N":{"tab":["n1"]}}})             // time-sheet
    addToLexicon({"pixel":{"N":{"tab":["n1"]}}})                   // angel
    addToLexicon({"megapixel":{"N":{"tab":["n1"]}}})               // angel

    addToLexicon({"euro":{"N":{"tab":["n1"]}}})                    // bistro
    addToLexicon({"something":{"N":{"tab":["n1"]}}})               // thing, already there as pronoun
    addToLexicon({"cupcake":{"N":{"tab":["n1"]}}})                 // bridecake
    addToLexicon({"burger":{"N":{"tab":["n1"]}}})                  // hamburger
    addToLexicon({"vegan":{"N":{"tab":["n1"]}}})                   // vegetarian

    // american English
    addToLexicon({"theater":{"N":{"tab":["n1"]}}});                // theatre
    addToLexicon({"color":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}})  // colour
    addToLexicon({"center":{"N":{"tab":["n1"]},"V":{"tab":"v3"}}}) // centre
    addToLexicon({"defense":{"N":{"tab":["n1"]}}})                 // defence
    addToLexicon({"neighborhood":{"N":{"tab":["n1"]}}})            // neighbourhood
    addToLexicon({"favor":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}})  // favour
    addToLexicon({"flavor":{"N":{"tab":["n1"]},"V":{"tab":"v1"}}}) // flavour
    addToLexicon({"summarise":{"V":{"tab":"v3"}}})                 // summarize
    addToLexicon({"civilisation":{"N":{"tab":["n1"]}}})            // civilization

    addToLexicon({"there":{"Pro":{"tab":["pn6"]}}})   // invariable pronoun
    addToLexicon({"all":{"Pro":{"tab":["pn6"]}}})
    addToLexicon({"one":{"Pro":{"tab":["pn6"]},"N":{"tab":"n1"}}})
    addToLexicon({"other":{"Pro":{"tab":["pn6"]}}})

    addToLexicon("this",{"D":{"tab":["d5"]}})
    addToLexicon("these",{"D":{"n":"p","tab":["d4"]}})  // should use lemma this

    //  but I am not always sure that the POS are always appropriate
    addToLexicon({"an":{"D":{"tab":["d4"]}}})   // should not have to do that...

    var prepositions=[
        "as","not","than","because","due"
    ];
    prepositions.forEach(function(prep){
        addToLexicon(prep,{"P":{"tab":["pp"]}})
    })

    var adverbs=[
        "how","when","there","why","much","where","up","down","most","more","on","off",
        "too","super","of","further","twice","for"
    ]
    adverbs.forEach(function(adv){
        addToLexicon(adv,{"Adv":{"tab":["b1"]}})
    })

    var adjectives=[
        "other","many","more","own","much","such","next","most","several","else","enough","less","top",
        "another","further","least","more","last","same","own","most","favorite","jewish",
        "terrorist"
    ];
    adjectives.forEach(function(adj){
        addToLexicon(adj,{"A":{"tab":["a1"]}})
    })

    // relating to a nation or noun
    // many of these are already there starting with a Capital
    // extracted with jq 'keys|.[]|select(match("^[A-Z].*(ish|an|ese)$"))' ~/Documents/GitHub/jsRealB/data/lexicon-dme.json
    
       var demonyms= [ "Afghan", "African", "Afro-American", "Afro-Asian", "Albanian", "Algerian",
       "Alsatian", "American", "Andorran", "Anglican", "Anglo-Indian", "Angolan", "Anguillan",
       "Antiguan", "Arabian", "Arcadian", "Argentinian", "Aryan", "Asian", "Augustan", "Australian",
       "Austrian", "Bahamian", "Barbadian", "Belgian", "Beninese", "Bermudan", "Bolivian", "Brazilian",
       "British", "Bruneian", "Bulgarian", "Burmese", "Burundian", "Bushman", "Caesarian", "Cambodian",
       "Cameroonian", "Canadian", "Catalan", "Caucasian", "Cesarean", "Chadian", "Chilean", "Chinese",
       "Christian", "Colombian", "Confucian", "Congolese", "Copernican", "Corinthian", "Cuban",
       "Cyclopean", "Cyprian", "Czechoslovakian", "Danish", "Djiboutian", "Dominican", "Dutchman",
       "Ecuadorian", "Egyptian", "Elizabethan", "Elysian", "English", "Englishman", "Englishwoman",
       "Eritrean", "Ethiopian", "Euclidean", "Eurasian", "European", "Eustachian", "Fabian",
       "Fallopian", "Fijian", "Finnish", "Flemish", "Franciscan", "Frenchman", "Frenchwoman",
       "Freudian", "G-man", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Gibraltarian",
       "Gilbertian", "Gordian", "Grecian", "Gregorian", "Grenadian", "Guatemalan", "Guinean",
       "Guyanese", "Haitian", "Hertzian", "Honduran", "Hungarian", "Indiaman", "Indian",
       "Indo-European", "Indonesian", "Iranian", "Irish", "Irishman", "Irishwoman", "Italian",
       "Jacobean", "Jamaican", "Japanese", "Javanese", "Jewish", "Jordanian", "Julian", "Kampuchean",
       "Kenyan", "Koran", "Korean", "Laotian", "Lebanese", "Liberian", "Libyan", "Lilliputian",
       "Lutheran", "Macedonian", "Madagascan", "Malawian", "Malayan", "Malaysian", "Malian", "Maltese",
       "Malthusian", "Martian", "Mauritanian", "Mauritian", "Mediterranean", "Mendelian",
       "Mephistophelian", "Mexican", "Mohammedan", "Mongolian", "Montserratian", "Moorish", "Moroccan",
       "Mozambican", "Muhammadan", "Namibian", "Nauruan", "Neapolitan", "Nepalese", "Newtonian",
       "Nicaraguan", "Nigerian", "Nipponese", "Norman", "Northman", "Norwegian", "Olympian",
       "Orangeman", "Oxonian", "Palestinian", "Panamanian", "Papuan", "Paraguayan", "Parisian",
       "Parmesan", "Parthian", "Persian", "Peruvian", "Polish", "Portuguese", "Presbyterian",
       "Prussian", "Pullman", "Rabelaisian", "Ramadan", "Rhenish", "Roman", "Romanian", "Romish",
       "Rotarian", "Ruritanian", "Russian", "Rwandan", "Sabahan", "Salvadorean", "Samaritan", "Samoan",
       "Sarawakian", "Satan", "Scandinavian", "Scotchman", "Scotchwoman", "Scotsman", "Scotswoman",
       "Scottish", "Senegalese", "Shakespearian", "Shavian", "Siamese", "Siberian", "Sicilian",
       "Singaporean", "Singhalese", "Sinhalese", "Slovenian", "Somalian", "Spanish", "Spartan",
       "Stygian", "Sudanese", "Sumatran", "Swedish", "Syrian", "Tahitian", "Taiwanese", "Tanzanian",
       "Terpsichorean", "Thespian", "Tibetan", "Tobagonian", "Togolese", "Tongan", "Trinidadian",
       "Trojan", "Tunisian", "Turkish", "Ugandan", "Unitarian", "Uruguayan", "Utopian", "Vatican",
       "Venetian", "Venezuelan", "Victorian", "Vietnamese", "Welshman", "Wesleyan", "Yiddish",
       "Yugoslavian", "Zairean", "Zambian", "Zimbabwean" ];
    
    const an={"A":{"tab":["a1"]},"N":{"tab":["n1"]}}
    demonyms.forEach(function(Demonym){
        // they should already be there...
        addToLexicon(Demonym,an);
        const demonym=Demonym.charAt(0).toLowerCase()+Demonym.substring(1);
        addToLexicon(demonym,an);
    })
    //////////////////

    // ajouts pour les textes de biologie (fréquence plus de 50 dans amr-ISI/amr-release-{dev|test|training}.txt)
    addToLexicon("mutate",{"V":{"tab":"v3"}});        // 1408
    addToLexicon("phosphorylate",{"V":{"tab":"v3"}}); // 1329
    addToLexicon("downregulate",{"V":{"tab":"v3"}});  // 160
    addToLexicon("overexpress",{"V":{"tab":"v2"}});   // 138
    addToLexicon("upregulate",{"V":{"tab":"v3"}});    // 121
    addToLexicon("culture",{"V":{"tab":"v3"}});       // 112
    addToLexicon("transfect",{"V":{"tab":"v1"}});     // 111
    addToLexicon("metastasize",{"V":{"tab":"v3"}});   // 62
    addToLexicon("immunoprecipitate",{"V":{"tab":"v3"}}); //52
    addToLexicon("phosphorylation",{"N":{"tab":["n5"]}});  //52
    addToLexicon("ubiquinate",{"V":{"tab":"v3"}});        //51
    // console.log("end of loadJSON",Object.keys(getLexicon()).length)
}