/*
* Scripts for new_game.html
*/
function disableSameTeam(dropdown) {
    if (dropdown.id === "left_team") {
        for (option of document.getElementsByClassName('right_team')) {
            if (option.value === dropdown.value) option.disabled = true
            else option.disabled = false
        }
    }
    else if (dropdown.id === "right_team") {
        for (option of document.getElementsByClassName('left_team')) {
            if (option.value === dropdown.value) option.disabled = true
            else option.disabled = false
        }
    }
}
