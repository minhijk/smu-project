function openSubMenu(key) {
  const subMenu = document.getElementById('subMenu');
  const title = document.getElementById('subMenuTitle');
  const content = document.getElementById('subMenuContent');

  const data = {
    'intro': { title: '상명소개', content: '서브 메뉴' },
    'admission': { title: '입학안내', content: '서브 메뉴' },
    'college': { title: '대학 · 대학원', content: '서브 메뉴' },
    'research': { title: '연구 · 산학', content: '서브 메뉴' },
    'academic': { title: '학사안내', content: '학사 일정', link: '/academic/calendar' },
    'life': { title: '대학생활', content: '서브 메뉴' },
    'course': { title: '수강신청', content: '서브 메뉴' },
    'login': { title: '로그인', content: '통합 로그인 연결' },
    'favorites': { title: '자주 사용하는 메뉴', content: '즐겨찾는 메뉴' },
    'search': { 
  title: '검색',  // 위에 "검색" 텍스트 없게
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
};

  const item = data[key];

  title.innerText = item?.title || '메뉴';

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

const prevBtn = document.querySelector('.prev');
if (prevBtn) {
  prevBtn.addEventListener('click', () => {
    let newIndex = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(newIndex);
  });
}

const nextBtn = document.querySelector('.next');
if (nextBtn) {
  nextBtn.addEventListener('click', () => {
    let newIndex = (currentSlide + 1) % totalSlides;
    showSlide(newIndex);
  });
}

dots.forEach((dot, idx) => {
  dot.addEventListener('click', () => {
    showSlide(idx);
  });
});

function loadNotices(campus, element) {
    // active 처리
    document.querySelectorAll('.tabs li').forEach(el => el.classList.remove('active'));
    element.parentElement.classList.add('active');

    fetch(`/api/notices/${campus}/`)
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('notice-list');
        list.innerHTML = '';
        if (data.length === 0) {
            list.innerHTML = '<li>공지사항이 없습니다.</li>';
        } else {
            data.forEach(n => {
                list.innerHTML += `
                <li style="padding: 10px 0; border-bottom: 1px solid #ddd;">
                    <a href="/notice?id=${n.id}" style="text-decoration: none; color: #0d47a1; font-size: 1.1em;">
                        ${n.title}
                    </a>
                    <div style="font-size: 0.9em; color: #aaa; margin-top: 4px;">
                        작성자: ${n.author} | 작성일: ${n.created_at}
                    </div>
                </li>`;
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const loginMenu = document.querySelector('.menu-item[data-key="login"]');

  // ✅ JWT 토큰 기반 로그인 상태 확인
  const isLoggedIn = !!localStorage.getItem("access");

  // ✅ 로그인 버튼 구성
  if (loginMenu) {
    if (isLoggedIn) {
      setLogoutUI(loginMenu);
    } else {
      loginMenu.textContent = 'LOGIN';
      loginMenu.removeAttribute('onclick');
      loginMenu.addEventListener('click', (e) => {
  e.preventDefault();
  const redirect_uri = encodeURIComponent("http://127.0.0.1:8000/handle-token/");
  window.location.href = `http://127.0.0.1:8001/login/?redirect_uri=${redirect_uri}`;
});

    }
  }

  // ✅ LOGOUT UI 구성 함수
  function setLogoutUI(loginMenu) {
    loginMenu.textContent = 'LOGOUT';
    loginMenu.removeAttribute('onclick');
    loginMenu.addEventListener('click', async (e) => {
      e.preventDefault();

      const refresh = localStorage.getItem("refresh");
      const access = localStorage.getItem("access");

      if (refresh && access) {
        try {
          await fetchWithAuth("http://127.0.0.1:8001/api/token/logout/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${access}`
            },
            body: JSON.stringify({ refresh })
          });
        } catch (err) {
          console.warn("로그아웃 실패:", err);
        }
      }

      // ✅ 로그아웃 시 토큰 제거 + 새로고침
      localStorage.clear();
      window.location.href = "/";
    });
  }
});

// ✅ 토큰을 자동으로 붙여주는 fetch 래퍼 함수
async function fetchWithAuth(url, options = {}) {
  const accessToken = localStorage.getItem("access");

  const headers = options.headers || {};

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  return fetch(url, {
    ...options,
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  });
}

function getDecodedJWT() {
  const token = localStorage.getItem("access");
  if (!token) return null;

  try {
    const payload = token.split('.')[1];
    const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    return decoded;
  } catch (e) {
    console.error("토큰 디코딩 실패:", e);
    return null;
  }
}

document.addEventListener('click', function(event) {
  const subMenu = document.getElementById('subMenu');
  const sidebar = document.querySelector('.sidebar');

  if (subMenu && subMenu.classList.contains('active')) {
    if (!subMenu.contains(event.target) && !sidebar.contains(event.target)) {
      closeSubMenu();
    }
  }
});

//프론트에서 공지 호출
async function updateNotice(noticeId, newTitle, newContent) {
  const response = await fetchWithAuth("/api/notice/update/", {
    method: "POST",
    body: JSON.stringify({
      id: noticeId,
      title: newTitle,
      content: newContent
    })
  });

  const result = await response.json();
  console.log(result);
}

async function createNotice(title, content, category) {
  const response = await fetchWithAuth("/api/notice/create/", {
    method: "POST",
    body: JSON.stringify({
      title: title,
      content: content,
      category: category
    })
  });

  const result = await response.json();
  console.log(result);
}

async function deleteNotice(id) {
  if (!confirm("정말 삭제하시겠습니까?")) return;

  const response = await fetchWithAuth("/api/notice/delete/", {
    method: "POST",
    body: JSON.stringify({ id })
  });

  const result = await response.json();
  if (response.ok) {
    alert("삭제되었습니다.");
    location.href = "/noticelist";
  } else {
    alert("삭제 실패: " + (result.error || "알 수 없는 오류"));
  }
}