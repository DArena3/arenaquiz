/*
* Scripts for add_team.html
*/
function changeInputNum(n) {
    let inputNum = document.getElementsByClassName('pname').length
    if (n < 1 || n > 8) return
    if (n < inputNum) {
        for (let i = Number(n) + 1; i <= inputNum; i++) {
            document.getElementById('player' + i).remove()
        }
    }
    else if (n > inputNum) {
        for (let i = inputNum + 1; i <= n; i++) {
            let input = document.createElement("INPUT")
            input.type = "text"
            input.name = "player" + i
            input.id = "player" + i
            input.classList.add("pname")
            input.classList.add("form-control")
            input.placeholder = "Player " + i
            document.getElementById('players').appendChild(input)
        }
    }
}
