// 메뉴 데이터 및 서브메뉴 열기 함수
function openSubMenu(key, event) {
  const subMenu = document.getElementById('subMenu');
  const title = document.getElementById('subMenuTitle');
  const content = document.getElementById('subMenuContent');

  // 메뉴 데이터 통합
  const data = {
    'intro': { title: '상명소개', content: '서브 메뉴' },
    'admission': { title: '입학안내', content: '서브 메뉴' },
    'college': { title: '대학 · 대학원', content: '서브 메뉴' },
    'research': { title: '연구 · 산학', content: '서브 메뉴' },
    'academic': { 
      title: '학사안내', 
      contents: [
        { text: '통합 공지', link: '/noticelist' },
        { text: '학사 일정', link: '/academic/calendar' }
      ] 
    },
    'life': { title: '대학생활', content: '서브 메뉴' },
    'course': { title: '수강신청', content: '서브 메뉴' },
    'login': { title: window.isLoggedIn === "true" ? 'LOGOUT' : 'LOGIN', content: '통합 로그인 연결' },
    'favorites': { 
      title: '', 
      content: `
        <div style='display:flex; flex-direction:column; align-items:center; gap:30px; color: white;'>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>🖱️</div>
            <div>수강신청</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>📑</div>
            <div>통합정보시스템</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>💻</div>
            <div>샘물포털</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>🎓</div>
            <div>e-campus</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>🏢</div>
            <div>office365</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:2em;'>📝</div>
            <div>e-포트폴리오</div>
          </div>
          <div style='margin-top:40px; display:flex; flex-direction:column; gap:20px;'>
            <a href="https://www.instagram.com/sangmyung_univ" target="_blank" style="text-decoration:none; color:white; text-align:center;">
              <div style='font-size:2em;'>📸</div>
              <div>인스타그램</div>
            </a>
            <a href="https://www.youtube.com/c/sangmyunguniversity" target="_blank" style="text-decoration:none; color:white; text-align:center;">
              <div style='font-size:2em;'>▶️</div>
              <div>유튜브</div>
            </a>
          </div>
        </div>
      `
    },
    'search': { 
      title: '',  // 제목 없이 검색창만
      content: `
        <input type='text' placeholder='검색' style='width: 100%; padding: 8px;'>
        <div style='margin-top:20px; display:flex; flex-wrap:wrap; gap:10px;'>
          <button class="tag-btn">취업</button>
          <button class="tag-btn">장학</button>
          <button class="tag-btn">창업</button>
          <button class="tag-btn">수강</button>
          <button class="tag-btn">성적</button>
          <button class="tag-btn">상생</button>
          <button class="tag-btn">학사운영</button>
          <button class="tag-btn">행사</button>
          <button class="tag-btn">국제</button>
          <button class="tag-btn">교양</button>
          <button class="tag-btn">교환학생</button>
          <button class="tag-btn">근로</button>
          <button class="tag-btn">ecampus</button>
          <button class="tag-btn">계절수업</button>
          <button class="tag-btn">비교과</button>
          <button class="tag-btn">상담</button>
        </div>
      `
    }
  };

  const item = data[key];

  title.innerText = item?.title || '메뉴';

  if (item?.contents && Array.isArray(item.contents)) {
    content.innerHTML = item.contents.map(c =>
      `<a href="${c.link}" style="text-decoration: none; color: inherit; display: block; padding: 10px 0;">${c.text}</a>`
    ).join('');
  } else if (item?.link) {
    content.innerHTML = `<a href="${item.link}" style="text-decoration: none; color: inherit;">${item.content}</a>`;
  } else {
    content.innerHTML = item?.content || '선택된 메뉴에 대한 설명이 없습니다.';
  }

  subMenu.classList.add('active');

  // 메뉴 활성화 클래스 토글 (선택 시)
  document.querySelectorAll('.menu-item.active').forEach(i => i.classList.remove('active'));
  if (event?.target?.classList) event.target.classList.add('active');
}

// 서브메뉴 닫기
function closeSubMenu() {
  const subMenu = document.getElementById('subMenu');
  subMenu.classList.remove('active');
  document.querySelectorAll('.menu-item.active').forEach(item => item.classList.remove('active'));
}

// 메뉴 클릭 핸들러
function handleMenuClick(key, event) {
  if (key === 'login') {
    if (window.isLoggedIn === "true") {
      // 로그아웃 처리
      window.location.href = '/logout';
    } else {
      // 로그인 새 창 열기
      window.open('/login', '_blank');
    }
  } else if (key === 'logout') {
    window.location.href = '/logout';
  } else {
    openSubMenu(key, event);
  }
}

// 문서 클릭 시 서브메뉴 밖 클릭하면 닫기
document.addEventListener('click', function(event) {
  const subMenu = document.getElementById('subMenu');
  const sidebar = document.querySelector('.sidebar');

  if (subMenu.classList.contains('active')) {
    if (!subMenu.contains(event.target) && !sidebar.contains(event.target)) {
      closeSubMenu();
    }
  }
});

// DOMContentLoaded 이벤트: 로그인 메뉴 상태 업데이트
document.addEventListener('DOMContentLoaded', () => {
  const loginMenu = document.querySelector('.menu-item[data-key="login"]');

  if (loginMenu) {
    if (window.isLoggedIn === "true") {
      loginMenu.textContent = 'LOGOUT';
      loginMenu.removeAttribute('onclick'); // 기존 onclick 제거
      loginMenu.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/logout';
      });
    } else {
      loginMenu.textContent = 'LOGIN';
      loginMenu.removeAttribute('onclick');
      loginMenu.addEventListener('click', (e) => {
        e.preventDefault();
        window.open('/login', '_blank');
      });
    }
  }
});


// 슬라이더 기능
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const totalSlides = slides.length;

function showSlide(n) {
  slides.forEach((slide, i) => {
    slide.classList.remove('active');
    dots[i].classList.remove('active');
    if (i === n) {
      slide.classList.add('active');
      dots[i].classList.add('active');
    }
  });
  currentSlide = n;
}

// 이전 슬라이드 버튼
document.querySelector('.prev').addEventListener('click', () => {
  let newIndex = (currentSlide - 1 + totalSlides) % totalSlides;
  showSlide(newIndex);
});

// 다음 슬라이드 버튼
document.querySelector('.next').addEventListener('click', () => {
  let newIndex = (currentSlide + 1) % totalSlides;
  showSlide(newIndex);
});

// 하단 도트 버튼 클릭 시
dots.forEach((dot, idx) => {
  dot.addEventListener('click', () => {
    showSlide(idx);
  });
});

// 초기 슬라이드 표시
document.addEventListener('DOMContentLoaded', () => {
  showSlide(0);
});
