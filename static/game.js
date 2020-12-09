/*
* Scripts for game.html
*/
function reset() {
    document.getElementById("submit_tossup").reset()
    document.getElementById("bonus-container").style.display = "none"
    for (e of document.getElementsByClassName("score-buttons")) {
        e.style.visibility = "hidden"
    }
    for (e of document.getElementsByClassName("btn")) {
        e.removeAttribute("disabled")
        e.classList.remove("active")
        e.removeAttribute("aria-pressed")
    }
}

function playerButtonClicked(element) {
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    p_id = element.parentElement.id
    document.getElementById(p_id + "-buttons").style.visibility = "visible"
    button_divs = element.parentElement.parentElement.getElementsByClassName("player-buttons")
    for (e of button_divs) {
        if (e.id != p_id) {
            e.getElementsByClassName("player-button")[0].disabled = "true"
        }
    }
}

function power(element) {
    document.getElementById("bonus-container").style.display = "flex"

    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    p_id = element.parentElement.parentElement.id
    document.getElementById("scoring-player").value = p_id
    document.getElementById("score").value = element.getAttribute("score")
    
    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "btn")

    b_group = element.parentElement
    b_group.getElementsByClassName("ten")[0].disabled = "true"
    b_group.getElementsByClassName("neg")[0].disabled = "true"
}

function score(element) {
    document.getElementById("bonus-container").style.display = "flex"

    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    p_id = element.parentElement.parentElement.id
    document.getElementById("scoring-player").value = p_id
    document.getElementById("score").value = element.getAttribute("score")

    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "btn")

    b_group = element.parentElement
    b_group.getElementsByClassName("power")[0].disabled = "true"
    b_group.getElementsByClassName("neg")[0].disabled = "true"
}

function neg(element) {
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    p_id = element.parentElement.parentElement.id
    document.getElementById("negging-player").value = p_id
    document.getElementById("neg-score").value = element.getAttribute("score")

    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "neg")

    b_group = element.parentElement
    b_group.getElementsByClassName("power")[0].disabled = "true"
    b_group.getElementsByClassName("ten")[0].disabled = "true"
}

function disableOtherTeamButtons(team_div, c_name) {
    if (team_div === "left-buttons") {
        for (e of document.getElementById("right-buttons").getElementsByClassName(c_name)) {
            if (!e.classList.contains("active")) {
                e.disabled = "true"
            }
        }
    }
    else if (team_div === "right-buttons") {
        for (e of document.getElementById("left-buttons").getElementsByClassName(c_name)) {
            if (!e.classList.contains("active")) {
                e.disabled = "true"
            }
        }
    }
}

function toggleCheckbox(id) {
    checkbox = document.getElementById(id)

    if (checkbox.checked === true) {
        checkbox.checked = false
    }
    else checkbox.checked = true
}

// From https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
// Prevents form submission on refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
