// const audio = document.querySelector('audio')
// const input = document.querySelector('input[name=name]')
// const form = document.querySelector('form')


// form.addEventListener('submit',(e)=>{
    
//     e.preventDefault()
//     let data = new FormData();
// data.append('name', input.value);;
// // add form input from hidden input elsewhere on the page
// data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
//     fetch("/files/", {
//         method: 'POST',
//         body: data,
//         credentials: 'same-origin',
//     })
//     .then(function(response) {
//         console.log(response)
//       return response.json()
//     }).then(function(data) {
//         console.log(data)
//         audio.src = 'data:audio/mpeg;base64,' + data.mp3; // this will be a string
//     });
// })


const state = {
    isForm:false,
    isEdit:false,
    id:0,
}

const formWrapper = document.querySelector('.track-form')
const addBtn = document.querySelector('.manage-tracks__btn-add')
const editBtns = document.querySelectorAll('.manage-tracks__btn-edit')

function setForm(){
    const heading = document.querySelector('.track-form h1')
    const form = document.querySelector('.track-form form')
    if(form){
        form.addEventListener('submit', async(e)=>{
        e.preventDefault()
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
        const urls = {
            add:'/add-track/',
            edit:'/update-track/'
        }
        var formData = new FormData(form)
        if(state.id){
            formData.append('id',state.id)
        }
        const url = state.isEdit ? urls.edit : urls.add
        fetch(url,{
                method:'POST',
                body:formData,
                headers:{
                    'X-CSRFToken': csrftoken
                }
        })
        .then(res => res.json())
        .then(data =>{
                form.reset()
                if(!state.isEdit){
                    heading.textContent = data.msg
                    setTimeout(() => {
                        heading.textContent = 'Add Track'
                    }, 2000);
                    }else{
                        heading.textContent =  data.msg
                        setTimeout(() => {
                        heading.textContent = 'Edit Track'
                        }, 2000);
                    }
            })
        })
    }
}


if(addBtn){
    addBtn.addEventListener('click',()=>{
        const heading = document.querySelector('.track-form h1')
        state.isEdit = false
        if(!state.isForm){
            formWrapper.style.display = 'block'
            addBtn.textContent = 'Hide'
            addBtn.style.backgroundColor = 'orangered'
            state.isForm = true
            heading.textContent = 'Add Track'
            setForm()
        }else{
            formWrapper.style.display = 'none'
            addBtn.textContent = 'Add Track'
            addBtn.style.backgroundColor = 'rgb(0, 255, 213)'
            state.isForm = false
        }
    })
}

if(editBtns){
    editBtns.forEach(b => {
        b.addEventListener('click',(e)=>{
        const heading = document.querySelector('.track-form h1')
        state.isEdit = true
        state.id = Number(e.target.parentElement.parentElement.querySelector('.manage-tracks__pk').textContent)
        if(!state.isForm){
            heading.textContent = 'Edit Track'
            formWrapper.style.display = 'block'
            addBtn.textContent = 'Hide'
            addBtn.style.backgroundColor = 'orangered'
            state.isForm = true
            setForm()
        }else{
            heading.textContent = 'Edit Track'
        }
    })
})
}