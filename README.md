# blog
- Django blog 만들기

# 📜요구사항

## 유저
- 회원가입
- 로그인
- 프로필
  - 닉네임 ❌
  - 수정 ❌

## 게시글
- 목록
- 작성
  - 권한 : 로그인
  - 사진 업로드
  - 조회수 ❌
- 상세
- 수정
- 삭제
  - 권한 : 로그인, 본인
  - "존재하지 않는 게시글입니다" 페이지 표시 ❌
- 검색 ❌
  - 주제나 태그에 따라 
  - 시간순 정렬

## 댓글 💬 ❌
- 권한 : 로그인
- 대댓글
  - 권한 : 로그인

## 정적파일(collectstatic) ❌
- 정적 파일들을 서버에서 모아서 제공하는 기능

## 번역 ❌
- 번역 기능은 구현되지 않음

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