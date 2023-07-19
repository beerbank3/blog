const form = document.querySelector('.input-form');
const categorySelect = document.querySelector('.categories');
const selectedCategories = new Set();
const selectedCategoriesDiv = document.querySelector('.category');
const existingCategories = selectedCategoriesDiv.querySelectorAll('dd');

const editor = new toastui.Editor({
    el: document.querySelector('#editor'),
    previewStyle: 'vertical',
    height: '500px',
    hideModeSwitch: true,
    initialValue: (typeof content !== 'undefined') ? content : '',
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
existingCategories.forEach(ddTag => {
    // categorySelect에서 해당 value를 찾아서 selectedCategories에 추가
    const categoryOption = Array.from(categorySelect.options).find(option => option.textContent.trim() === ddTag.textContent.trim());
    if (categoryOption) {
        selectedCategories.add(categoryOption.value);

        // Remove Button 생성
        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.className = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded';
        removeButton.addEventListener('click', function() {
            const categoryId = categoryOption.value;
            selectedCategories.delete(categoryId); // 해당 카테고리 삭제 (Set에서도 삭제)
            selectedCategoriesDiv.removeChild(ddTag); // 해당 카테고리 삭제 (화면에서 삭제)

            // form으로 전달된 해당 카테고리도 삭제
            const inputElement = document.querySelector(`input[name="categories"][value="${categoryId}"]`);
            if (inputElement) {
                inputElement.remove();
            }
        });

        ddTag.appendChild(removeButton);

        const inputElement = document.createElement('input');
        inputElement.type = 'hidden';
        inputElement.name = 'categories';
        inputElement.value = categoryOption.value;
        document.querySelector('form').appendChild(inputElement);
    }
});
categorySelect.addEventListener('change', function() {
    const selectedCategory = categorySelect.options[categorySelect.selectedIndex];
    if (selectedCategory.value !== '') {
        // 이미 추가된 카테고리인지 확인
        console.log(selectedCategories)
        if (!selectedCategories.has(selectedCategory.value)) {
            // 선택한 카테고리를 추가
            selectedCategories.add(selectedCategory.value);

            // <dd> 태그 추가
            const ddTag = document.createElement('dd');
            ddTag.textContent = selectedCategory.textContent;

            // x 표시 추가
            const removeButton = document.createElement('span');
            removeButton.textContent = 'x';
            removeButton.className = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded';
            removeButton.addEventListener('click', function() {
                selectedCategories.delete(selectedCategory.value); // 해당 카테고리 삭제 (Set에서도 삭제)
                selectedCategoriesDiv.removeChild(ddTag); // 해당 카테고리 삭제 (화면에서 삭제)

                // form으로 전달된 해당 카테고리도 삭제
                const inputElement = document.querySelector(`input[name="category"][value="${selectedCategory.value}"]`);
                if (inputElement) {
                    inputElement.remove();
                }
            });

            ddTag.appendChild(removeButton);
            selectedCategoriesDiv.appendChild(ddTag);

            // 추가된 카테고리 값을 form으로 전달
            const inputElement = document.createElement('input');
            inputElement.type = 'hidden';
            inputElement.name = 'categories';
            inputElement.value = selectedCategory.value;
            document.querySelector('form').appendChild(inputElement);
        }
    }
});

form.addEventListener('submit', (e) => {
    e.preventDefault(); // 기본 폼 제출 동작 방지
  
    const formData = new FormData(form); // 폼 데이터 생성
    formData.append('content',editor.getMarkdown());
  
    fetch(form.action, {
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