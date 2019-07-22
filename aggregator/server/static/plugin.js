function showAddPlugin() {
    let menu = document.getElementById("add-plugin-menu")
    let box = document.getElementById("add-plugin-button").getBoundingClientRect()
    menu.style.top = box.bottom + window.scrollY + 'px'
    menu.style.left = box.left + window.scrollX + 'px'
    menu.style.visibility = "visible"
}

function addPlugin(name) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 
        if (this.status == 200) {
            document.location.reload(true)
        }
    }
    xhr.open("POST", window.location.href + "add-plugin/" + name, true)
    xhr.send()
}

function removePlugin(plugin) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 
        if (this.status == 200) {
            document.location.reload(true)
        }
    }
    xhr.open("DELETE", window.location.href + "remove-plugin/" + plugin, true)
    xhr.send()
}

function showPluginSettings(plugin) {
    let item = document.getElementById(`plugin-settings-${plugin}`)
    let box = document.getElementById(`plugin-${ plugin }`).getElementsByClassName('plugin-header')[0].getBoundingClientRect()
    item.style.top = box.bottom + window.scrollY + 'px'
    item.style.left = box.left + window.scrollX + 'px'
    item.style.visibility = "visible"
}

function saveParam(plugin, param) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 
        if (this.status == 200) {
            let saved = document.getElementById(`param-${plugin}-${param}-saved`)
            saved.innerHTML = "OK"
        }
    }
    let input = document.getElementById(`param-${plugin}-${param}-input`)
    let value
    if (input.type == "checkbox") {
        value = input.checked
    } else {
        value = input.value
    }
    xhr.open("POST", `${window.location.href}save-param/${plugin}/${param}/${value}` , true)
    xhr.send()
}
