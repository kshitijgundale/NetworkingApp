var num_page = 1;
var curr_user_id = null;
document.addEventListener('DOMContentLoaded', ()=>{
    load_allposts();
    document.querySelector('.following.nav-link').onclick = () => {
        num_page = 1;
        load_allposts("following");
    };
    document.addEventListener('click', (e)=>{
        if(e.target.className == "profile-btn btn btn-link"){
            load_profile(e.target.dataset.id);
        }
        else if(e.target.className == "like-btn"){
            fetch(`/like/${e.target.dataset.id}`, {method: 'PUT'})
            .then(response => response.json())
            .then(data => {
                let span = e.target.parentElement.querySelector('.like-status')
                let num = parseInt(span.innerHTML);
                if(data === "Like"){
                    num = num - 1;
                }
                else{
                    num = num + 1;
                }
                span.innerHTML = num;
                e.target.innerHTML = data
            });
        }
        else if(e.target.id == "follow-btn"){
            fetch(`/follow/${e.target.dataset.id}`, {method: 'PUT'})
            .then(response => response.json())
            .then(data => {
                let span = e.target.parentElement.parentElement.querySelector('#s2');
                let num = parseInt(span.innerHTML);
                if(data === "Follow"){
                    num = num - 1;
                }
                else{
                    num = num + 1;
                }
                span.innerHTML = num + " followers";
                e.target.innerHTML = data;
            });
        }
        else if(e.target.className == "edit-btn"){
            let div = e.target.parentElement.parentElement;
            div.querySelector('.p-container').style.display = 'none';
            div.querySelector('.edit-btn-view').style.display = 'none';
            s = `<textarea class="edit-text" rows="3" cols="70">${div.querySelector(".post-body").innerHTML.trim()}</textarea>` +
                    `<button class="save-btn" data-postid=${e.target.dataset.postid}> Save </button>`
                
            let d = document.createElement('div');
            d.className = "edit-view"
            d.innerHTML = s;
            r = div.querySelector('.edit-view')
            if(div.querySelector('.edit-view') != undefined){
                div.replaceChild(d, div.querySelector('.edit-view'));
            }
            else{
                div.appendChild(d);
            }
        }
        else if(e.target.className == "save-btn"){
            fetch(`/edit/${e.target.dataset.postid}`, {
                method: "PUT",
                body: JSON.stringify({
                    text: e.target.parentElement.querySelector('.edit-text').value
                })
            })
            .then(response=>response.json)
            .then(data=>{
                let div = e.target.parentElement.parentElement;
                div.querySelector('.p-container').style.display = 'block';
                div.querySelector('.edit-btn-view').style.display = 'block';
                let ed = div.querySelector('.edit-view')
                ed.style.display = 'none';
                div.querySelector('.post-body').innerHTML = ed.querySelector('.edit-text').value
            });
        }
        else if(e.target.id == "btn-next"){
            num_page = num_page + 1;
            load_allposts(curr_user_id);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        else if(e.target.id == "btn-prev"){
            num_page = num_page - 1;
            load_allposts(curr_user_id);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
})

function load_allposts(user_id=null){
    document.querySelector('#profile-page').style.display = 'none';

    curr_user_id = user_id;
    var a = null
    if(user_id === null){
        a = fetch(`/posts/${num_page}`)
    }
    else{
        a = fetch(`/posts/${user_id}/${num_page}`)
    }
    a
    .then(response => response.json())
    .then(posts => {
        var enc = document.createElement('div');
        enc.className = "post-enc";
        let f = '';
        posts[0].forEach(element => {
            let s = ``;
            s = `<div class="p-container">
                    <div>
                        <button type="button" class="profile-btn btn btn-link" data-id=${element[0].author_id}> ${element[0].author_name} </button>
                    </div>
                    <div class="post-body">
                        ${element[0].body}
                    </div>
                    <div class="p1">
                        <span class="like-status">${element[0].likes}</span>  people like this
                        <button class="like-btn" data-id=${element[0].post_id}>${element[1]}</button>
                    </div>
                    <div class="post-time">
                        ${element[0].timestamp}
                    </div>
                </div>`;
            let a = '';
            if(element[2] === true){
                a = `<div class="edit-btn-view">
                        <button class="edit-btn" data-postid=${element[0].post_id}> Edit </button>
                    </div>`
            }
            f += '<div class="fcon">' + s + a + '</div>';
        });
        let btns = '';
        let btn_next = '<button id="btn-next">Next</button>';
        let btn_previous = '<button id="btn-prev">Previous</button>'
        if(posts[1] === 1){
            btns = '';
        }
        else if(num_page === 1){
            btns = btn_next;
        }
        else if(num_page === posts[1]){
            btns = btn_previous;
        }
        else{
            btns = btn_previous + btn_next;
        }
        let pag = '<div id="pag">' + btns + '</div>';
        enc.innerHTML = f + pag;
        document.querySelector('#all-posts').innerHTML = enc.outerHTML;
    });
}

function load_profile(id){
    fetch(`/profile/${id}`)
    .then(response => response.json())
    .then(data => {
        var enc = document.createElement('div');
        enc.className = "profile-enc";
        let s = '';
        s = `<div id="profile-name">
                <div>
                    <div id="pn1">
                        ${data[0].name}
                    </div>        
                    <div id="pn2">
                        <span> ${data[0].num_following} following </span>
                        <span id="s2"> ${data[0].num_followers} followers </span>
                    </div>
                </div>
             </div>`
        if(data[1] === true){
            s += `<div id="follow-view">
                    <button id="follow-btn" data-id=${data[0].id}>${data[2]}</button>
                  </div>`
        }
        enc.innerHTML = s;
        document.querySelector('#profile-page').innerHTML = enc.outerHTML;
        num_page = 1;
        load_allposts(data[0].id);
        document.querySelector('#profile-page').style.display = 'block';  
    });
}
