
function init() {
    document.body.style.border = "25px solid green";

    console.log( "loading script...")

let observedElem = document.getElementsByTagName("wc-vertical-move-list");
var parseMoves = (el) => {
    move_list = []

    var childList = el.children;

    for (let item of childList){
        let moveData = item.children;
        for (let m of moveData) {
            data = {}
            let att = { ...m.attributes};
            let keys = Object.keys(att);
            for (let i = 0; i < keys.length; i++){
                let found_att = att[i]
                if ( found_att.name == "data-ply"){
                    data['ply'] = found_att.nodeValue
                }
            }
            data['move'] = m.innerHTML
            move_list.push(data)
        }
    }
    
    let moves_str = ""

    for (let i = 0; i < move_list.length; i++) {
        const elem = move_list[i];
        moves_str += `${elem['move']}`
        if (i < move_list.length-1){
            moves_str += "_"
        }
    }
    console.log(JSON.stringify({moves: moves_str}));
    
    fetch("http://127.0.0.1:5000/moves", { 
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        mode: 'cors',
        body: JSON.stringify({moves: moves_str}) //return json
    }).then((response) => {
        // console.log("res:", response)
    }).catch((err)=> {
        console.log('failed to send moves to server: ', err)
    })
}

var mutationObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
         if(mutation.addedNodes.length != 0) {
            parseMoves(observedElem[0])
        }
    });
});

mutationObserver.observe(observedElem[0], { subtree: true, childList: true});
} 

init();

