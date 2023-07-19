const form = document.querySelector('.input-form');


const editor = new toastui.Editor({
    el: document.querySelector('#editor'),
    previewStyle: 'vertical',
    height: '500px',
    hideModeSwitch: true,
    hooks: {
      addImageBlobHook: (blob, callback) => uploadImages(blob, callback)
    }
});

const uploadImages = (blob, callback) => {
    let formData = new FormData();
    formData.append("images", blob);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/blog/upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(function(response) {
    if (response.ok) {
        const promise = response.json();
        const getData = () => {
            return promise.then((appData) => {
                return appData['image_path'];
            });
        };
        return getData();
    } else {
        throw new Error('image_load_fail');
    }
    })
    .then(function(data) {
    callback(data);
    })
    .catch(function(error) {
    callback(error.message);
    });
}

form.addEventListener('submit', (e) => {
    e.preventDefault(); // 기본 폼 제출 동작 방지
  
    const formData = new FormData(form); // 폼 데이터 생성
    formData.append('content',editor.getMarkdown());
  
    fetch('/blog/write/', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      window.location.href = '/blog';
    })
    .catch(error => {
      console.error('업로드 실패:', error);
    });
});