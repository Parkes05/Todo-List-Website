const sortableList = document.querySelector('.sortable-list');
const items = document.querySelectorAll('.item');


items.forEach(item => {
    item.addEventListener('dragstart', () => {
        setTimeout(() => item.classList.add('dragging'), 0);
    });
    item.addEventListener('dragend', () => item.classList.remove('dragging'));
});

const initSortableList = (e) => {
    e.preventDefault();
    const draggingItem = document.querySelector('.dragging');
    let siblings = [...sortableList.querySelectorAll('.item:not(.dragging')];
    let nextSibling = siblings.find(siblings => {
        return e.clientY <= siblings.offsetTop + siblings.offsetHeight / 2;
    });
    
    sortableList.insertBefore(draggingItem, nextSibling)
}

sortableList.addEventListener('dragover', initSortableList)
sortableList.addEventListener('dragenter', e => e.preventDefault())



function checkAll(o) {
    var boxes = document.getElementsByTagName("input");
    for (var x = 0; x < boxes.length; x++) {
        var obj = boxes[x];
        if (obj.type == "checkbox") {
            if (obj.name != "check")
            obj.checked = o.checked;
        }
    }
}   



function removeItem(num) {
    var a = document.getElementById("list");
    var item = document.getElementById(num);
    a.removeChild(item);
}



// function addItem() {
//     var a = document.getElementById("list");
//     var candidate = document.getElementById("candidate");
//     var li = document.createElement("li");
//     li.setAttribute('id', candidate.value);
//     li.setAttribute('class', 'item');
//     li.setAttribute('draggable', 'true');

//     let img = document.createElement('img');
//     img.src ="/static/svg/three-dots-vertical.svg";
//     let img1 = document.createElement('img');
//     img.src ="/static/svg/three-dots-vertical.svg";
//     var div = document.createElement("div");
//     div.setAttribute('class', 'details');

//     var input = document.createElement('input');
//     input.setAttribute('type', 'checkbox');
//     input.setAttribute('name', 'chk');
    
//     div.appendChild(input);
//     li.appendChild(img);
//     li.appendChild(img1);
//     li.appendChild(div);
//     li.appendChild(document.createTextNode(candidate.value));
//     a.appendChild(li);
// }



function sendItem() {
    var myValue = [...sortableList.querySelectorAll('.item:not(.dragging')]; 
    var element = document.getElementById("result");
    var x = []

    for (var i = 0; i < myValue. length; i++) {
        x += myValue[i].id;
    }

    element.value = x
}



var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})