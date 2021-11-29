var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var bookId = this.dataset.book
        var action = this.dataset.action
        console.log('bookId: ', bookId, 'action: ', action)

        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            alert('Not logged in')
        }
        else{
            updateUserOrder(bookId, action)
        }
    })
}


function updateUserOrder(bookId, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'bookId': bookId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}