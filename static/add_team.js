/*
* Scripts for add_team.html
*/

// Function that dynamically changes the number of player name inputs
// in the add_team form.
function changeInputNum(n) {
    let inputNum = document.getElementsByClassName('pname').length
    if (n < 1 || n > 8) return
    // If selected value < number of inputs, remove extra inputs
    if (n < inputNum) {
        for (let i = Number(n) + 1; i <= inputNum; i++) {
            document.getElementById('player' + i).remove()
        }
    }
    // If selected value > number of inputs, create extra inputs
    else if (n > inputNum) {
        for (let i = inputNum + 1; i <= n; i++) {
            // Set props to match that of existing inputs
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
