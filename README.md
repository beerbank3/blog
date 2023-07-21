# blog
- blog 만들기
## 기능

- 회원가입, 로그인
- 게시글(CRUD)

## 데이터베이스 모델링
![ERD](/README/ERD.png)

## 프로젝트 구조
```
📁 app/
├─📁 blog/
│  ├─📁 migrations/
│  └─📁 templates/
│    └─📁 blog/
├─📁 media/
│  ├─📁 image/
│  ├─📁 images/
│  └─📁 profile_images/
├─📁 README/
├─📁 static/
│  ├─📁 assets/
│  ├─📁 css/
│  ├─📁 images/
│  └─📁 js/
├─📁 templates/
├─📁 user/
│  ├─📁 migrations/
│  └─📁 templates/
│     └─📁 user/
└─📁 venv/
```

## 페이지
메인 페이지
![main](/README/main.png)

로그인후 페이지
![main-blog](/README/main-blog.png)

- 로그인
![login](/README/login.png)
- 회원가입
![register](/README/register.png)

- 글쓰기
![write](/README/write.png)
- 상세페이지
![detail](/README/detail.png)
- 수정
![edit](/README/edit.png)

## 오류 수정
- 유저 이름이라서 return Null 오류  
![user_str](/README/user_str.png)

- form 제출 형태 변경  
```
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    formData.append('content',editor.getMarkdown());

    fetch('/blog/write/', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      console.log('업로드 완료:', data);
    })
    .catch(error => {
      console.error('업로드 실패:', error);
    });
});
```

```
form.addEventListener('submit', (e) => {
    const contentInput = document.querySelector('.contentInput');
    contentInput.value = (typeof editor.getMarkdown() !== 'undefined') ? editor.getMarkdown() : '';
});
```

- toast ui editor initialValue사용시 개행이 있으면 값이안나옴  
![toast error](/README/toast_error.png)

- 카테고리 오류  
```
categories = models.ManyToManyField(Category)
```
![category_form](/README/category_form.png)

**write code**  
![write_code](/README/write_code.png)

**forms code**  
![forms_code](/README/forms_code.png)