/**
 * chessReader.js
 * This file contains the logic for the web extension.
 * The web extension scrapes chess.com for incoming moves and sends the move to backend.
 */
async function run() {
    //this border exists to give a visual indicator for if the extension is active or not.
    document.body.style.border = "8px solid green"; 
    console.log("loading script...");
    let observedElem = document.getElementsByTagName("wc-vertical-move-list");

    // parseMoves is executed whenever a move is made. 
    var parseMoves = (el) => {
        move_list = []
        var childList = el.children;

        //strip move from CSS element, store in data dictionary 
        for (let item of childList) {
            let moveData = item.children;
            for (let m of moveData) {
                data = {}
                let att = { ...m.attributes };
                let keys = Object.keys(att);
                for (let i = 0; i < keys.length; i++) {
                    let found_att = att[i]
                    if (found_att.name == "data-ply") {
                        data['ply'] = found_att.nodeValue
                    }
                }
                data['move'] = m.innerHTML
                move_list.push(data)
            }
        }

        let moves_str = ""

        //convert moves to string
        for (let i = 0; i < move_list.length; i++) {
            const elem = move_list[i];
            moves_str += `${elem['move']}`
            if (i < move_list.length - 1) {
                moves_str += "_"
            }
        }
        // send moves to backend server. 
        console.log(JSON.stringify({ moves: moves_str }));
        try {
            res = fetch("http://127.0.0.1:5000/moves", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors',
                body: JSON.stringify({ moves: moves_str }), //return json
            })
        } catch (e) {
            console.log('failed to send moves to server: ', e)
        }
        console.log("res:", res)
    }

    var mutationObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            // Check that the mutation is derived from black / white pieces moving. 
            // When a move is made chess.com has a seperate mutation to increment the move number.
            // Without this check parseMoves() is triggered twice per move which resulted in duplicate database entries. 
            const validMutation = Array.from(mutation.addedNodes).some(node =>
                node.classList && (node.classList.contains('black') || node.classList.contains('white')));

            if (validMutation && mutation.type === "childList") {
                parseMoves(observedElem[0]);
            }
        });
    });
    
    mutationObserver.observe(observedElem[0], { subtree: true, childList: true });
}

run();