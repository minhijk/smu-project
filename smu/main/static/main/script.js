function openSubMenu(key) {
  const subMenu = document.getElementById('subMenu');
  const title = document.getElementById('subMenuTitle');
  const content = document.getElementById('subMenuContent');

  const data = {
    'intro': { title: '상명소개', content: '연혁'},
    'admission': { title: '입학안내', content: '대학 입학' },
    'college': { title: '대학 · 대학원', content: '대학 소개' },
    'research': { title: '연구 · 산학', content: '연구 협력 기관' },
    'academic': { title: '학사안내',content: '학사 일정', link: '/academic/calendar'},
    'life': { title: '대학생활', content: '통합 공지',link: '/noticelist'},
    'course': { title: '수강신청', content: '수강 신청 페이지' },
    'search': { 
      title: '', 
      content: `
        <input type='text' placeholder='검색'>
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
    },
    'favorites': {
    title: '자주 사용하는 메뉴',
    content: `
      <div style='display:flex; flex-direction:column; align-items:center; gap:30px;'>
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
        
        <!-- 아래 소셜 영역 -->
        <div style='margin-top:40px; display:flex; flex-direction:column; gap:20px;'>
        <a href="https://www.instagram.com/sangmyung_univ" target="_blank" style="text-decoration:none; color:white; text-align:center;">
          <div style='text-align:center;'>
            <div style='font-size:2em;'>📸</div>
            <div>인스타그램</div>
          </div>
          <div style='text-align:center;'>
          <a href="https://www.youtube.com/c/sangmyunguniversity" target="_blank" style="text-decoration:none; color:white; text-align:center;">
            <div style='font-size:2em;'>▶️</div>
            <div>유튜브</div>
          </div>
        </div>
      </div>
    `
  }
    // ... 다른 메뉴 생략
  };

  const item = data[key];

  title.innerText = (key === 'search') ? '' : (item?.title || '메뉴');

  if (item?.link) {
    content.innerHTML = `<a href="${item.link}" style="text-decoration: none; color: inherit;">${item.content}</a>`;
  } else {
    content.innerHTML = item?.content || '선택된 메뉴에 대한 설명이 없습니다.';
  }

  subMenu.classList.add('active');

  if (key === 'search') {
    setTimeout(() => {
      document.querySelectorAll('.tag-btn').forEach(btn => {
        btn.addEventListener('click', function () {
          const tag = encodeURIComponent(this.textContent.trim());
          window.location.href = '/noticelist?search=' + tag;
        });
      });

      const input = document.querySelector('#subMenuContent input[type="text"]');
      if (input) {
        input.addEventListener('keydown', function(e) {
          if (e.key === 'Enter') {
            e.preventDefault();
            const query = encodeURIComponent(this.value.trim());
            if (query) {
              window.location.href = '/noticelist?search=' + query;
            }
          }
        });
      }
    }, 0);
  }
}

function closeSubMenu() {
  const subMenu = document.getElementById('subMenu');
  subMenu.classList.remove('active');
}

// 슬라이더
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

document.querySelector('.prev').addEventListener('click', () => {
  let newIndex = (currentSlide - 1 + totalSlides) % totalSlides;
  showSlide(newIndex);
});

document.querySelector('.next').addEventListener('click', () => {
  let newIndex = (currentSlide + 1) % totalSlides;
  showSlide(newIndex);
});

dots.forEach((dot, idx) => {
  dot.addEventListener('click', () => {
    showSlide(idx);
  });
});

function loadNotices(category, tabElement) {
  document.querySelectorAll('.tabs li').forEach(li => li.classList.remove('active'));
  tabElement.parentElement.classList.add('active');

  const searchInput = document.querySelector('input[name="q"]');
  const searchText = searchInput ? searchInput.value : '';

  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (searchText) params.append('search', searchText);

  fetch(`/noticelist?${params.toString()}`, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(response => response.json())
  .then(data => {
    const list = document.getElementById('notice-list');
    list.innerHTML = '';

    if (data.length === 0) {
      list.innerHTML = '<li>공지사항이 없습니다.</li>';
      return;
    }

    data.forEach(notice => {
      const li = document.createElement('li');
      li.style.padding = '12px 0';
      li.style.borderBottom = '1px solid #333';
      li.innerHTML = `
        <a href="/notice?id=${notice.id}" style="text-decoration: none; color: black; font-size: 1.1em;">
          ${notice.title}
        </a>
        <div style="font-size: 0.9em; color: #555; margin-top: 4px;">
          작성자: ${notice.author} | 작성일: ${notice.created_at}
        </div>
      `;
      list.appendChild(li);
    });
  })
  .catch(error => {
    console.error('공지사항 로딩 중 오류 발생:', error);
  });
}

function searchByCategory(button) {
    const category = button.textContent.trim();
    const query = encodeURIComponent(category);
    window.location.href = `/noticelist?search=${query}`;
}

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
        // ✅ 팝업창으로 로그인 띄우기
        window.open(
          '/login/',
          'loginPopup',
          'width=480,height=600,resizable=no,scrollbars=no'
        );
      });
    }
  }
});

document.addEventListener('click', function(event) {
  const subMenu = document.getElementById('subMenu');
  const sidebar = document.querySelector('.sidebar');

  if (subMenu && subMenu.classList.contains('active')) {
    if (!subMenu.contains(event.target) && !sidebar.contains(event.target)) {
      closeSubMenu();
    }
  }
});

