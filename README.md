# blog
- Django blog 만들기

# 📜요구사항

## 유저
- 회원가입
- 로그인
- 프로필
  - 수정
    - (이름, 내용,프로필 이미지, 카테고리)

## 게시글
- 목록
- 작성
  - 권한 : 로그인
  - 사진 업로드
  - 조회수 (중복 처리 X)
- 상세
- 수정
- 삭제
  - 권한 : 로그인, 본인
  - "존재하지 않는 게시글입니다" 페이지 표시 ❌
- 공개,비공개
- 검색 ❌
  - 주제나 태그에 따라 
  - 시간순 정렬

## 댓글 💬 ❌
- 권한 : 로그인
- 대댓글
  - 권한 : 로그인

## 로그 
- 액션, 시간, Post, User
- User가 읽은 Post 체크
## 정적파일(collectstatic) ❌
- 정적 파일들을 서버에서 모아서 제공하는 기능

## 번역 ❌
- 번역 기능은 구현되지 않음

# 데이터베이스 모델링
![ERD](/README/ERD.png)

# 프로젝트 구조
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

# 페이지
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

# 오류 수정
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

**forms code 에러**
- 데이터베이스 삭제직후 에러 발생

문제의 blog.forms 코드
```
categories = forms.MultipleChoiceField(
    choices=Category.objects.all().values_list('id', 'name'),  # 카테고리 선택지를 가져와 사용
    widget=forms.MultipleHiddenInput,
    required=False
)
```
해당 코드떄문에 데이터베이스를 삭제하고 난뒤 
```
python manage.py makemigrations
python manage.py migrate
```
위의 명령어 사용시 아래 오류 표출
```
django.db.utils.OperationalError: no such table: blog_category
```

데이터베이스를 생성한뒤에는 migrate이 정상적으로 작동되나 데이터베이스 삭제직후 에러 발생

테이블이 생성되기 전 모델에 대한 데이터를 조회하면서 에러가 나는것으로 예상

해결방법: 문제의 코드를 주석처리후 migrate완료후 주석 제거
