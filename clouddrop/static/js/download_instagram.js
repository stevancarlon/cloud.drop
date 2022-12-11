document.addEventListener('DOMContentLoaded', function(){

    const ok_btn = document.getElementById("ok-btn")
    const url_input = document.getElementById("url-input")

    ok_btn.addEventListener('click', () => download(url_input))

    console.log('download instagram script loaded')
});

async function download(url_input) {
    console.log('download function debug')
    // console.log(url_input.value)

    const loading_div = document.getElementById('loading-box')
    const loading_div_2 = document.getElementById('loading-box-2')
    const buttons_div = document.getElementById('buttons-div')
    const thumbnail_div = document.getElementById('thumbnail-div')


    loading_div_2.style.display = 'none'
    loading_div.style.display = 'flex'
    loading_div.classList.add('animate')
    // loading_div.style.transform = 'scale(1.05)'
    // loading_div.style.transition = '1s'

    var url = url_input.value

    const loading_img = document.getElementById('loading-img')
    const loading_label = document.getElementById('loading-label')
    const video_title = document.getElementById('video-title')
    const video_duration = document.getElementById('video-duration')

    url = url.split("/")
    // url = url[3]
    // url = url.split('watch?v=')
    // url = url[1]
    url = url[4]
    console.log(url)
    

    fetch('/download_instagram/' + url, {
        method: 'GET'
      })
      .then(response => response.json())
      .then(result => {
        console.log(result)

        const download_btn = document.createElement('button')
        download_btn.innerHTML = 'Download'
        download_btn.classList.add('download-btn')
        download_btn.setAttribute("id", "download-btn")
        download_btn.addEventListener('click', () => generate_link(url))
        buttons_div.appendChild(download_btn)
        loading_img.remove()
        loading_label.remove()
        loading_div.style.display = 'none'
        loading_div_2.style.display = 'flex'
        thumbnail_div.innerHTML = '<img src="static/ig_thumbs/' + url + '.jpg"  height="100px" width="70px" style="border-radius: 5px">'
        video_title.innerHTML = result.title + '...'
        video_duration.innerHTML = 'From: ' + result.author
      })


    //   .then(response => response.json())
    //     .then(result => {
    //         console.log(result)


    //         const download_btn = document.createElement('button')
    //         const download_btn_2 = document.createElement('button')

    //         download_btn.innerHTML = 'Download 720p'
    //         download_btn.classList.add('download-btn')
    //         download_btn.setAttribute("id", "download-btn")
    //         // download_btn.addEventListener('click', () => generate_link_720p(url))

    //         // download_btn_2.innerHTML = 'Download 360p'
    //         // download_btn_2.classList.add('download-btn')
    //         // download_btn_2.setAttribute("id", "download-btn-2")
    //         // download_btn_2.addEventListener('click', () => generate_link_360p(url))

    //         // buttons_div.appendChild(download_btn_2)
    //         buttons_div.appendChild(download_btn)
    //         loading_img.remove()
    //         loading_label.remove()
    //         loading_div.style.display = 'none'
    //         loading_div_2.style.display = 'flex'

    //         // loading_div_2.style.flexDirection = 'column'
    //         // loading_div_2.classList.add('animate-2')
    //         // thumbnail_div.innerHTML = '<img src="' + result.thumbnail + '" class="thumbnail-img">'
    //         // video_title.innerHTML = result.title
    //         // video_duration.innerHTML = result.length
    //     })   
}

function generate_link(url) {
    console.log(url)
    fetch('/generate_instagram_link/' + url, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })

    window.location='http://127.0.0.1:8000/generate_instagram_link/' + url 

}


// function generate_link_720p(url) {
//     console.log('Debug: ', url)
//     fetch('/generate_link/' + url, {
//         method: 'GET'
//     })
//     .then(response => response.json())
//     .then(result => {
//         console.log(result)
//     })

//     window.location='http://127.0.0.1:8000/generate_youtube_link/' + url + '_res_720p'

//     // const download_btn = document.getElementById('download-btn')
//     // download_btn.addEventListener('click', function(){
//     //     window.location='http://127.0.0.1:8000/generate_link/' + url
//     // })

// }
