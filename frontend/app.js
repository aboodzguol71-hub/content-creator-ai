const generateBtn = document.getElementById('generateBtn');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const scriptOutput = document.getElementById('scriptOutput');
const socialPlan = document.getElementById('socialPlan');
const videoPreview = document.getElementById('videoPreview');

generateBtn.addEventListener('click', async () => {
  const topic = document.getElementById('topic').value.trim();
  const tone = document.getElementById('tone').value;
  const platform = document.getElementById('platform').value;

  if (!topic) {
    statusEl.textContent = 'يرجى إدخال موضوع المحتوى أولاً';
    return;
  }

  statusEl.textContent = 'جارٍ إنشاء المحتوى...';

  try {
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic,
        tone,
        platform,
        language: 'ar',
      }),
    });

    const data = await response.json();
    scriptOutput.textContent = data.script;
    socialPlan.innerHTML = `
      <p><strong>المنصة:</strong> ${data.social_plan.platform}</p>
      <p><strong>الخطاف:</strong> ${data.social_plan.hook}</p>
      <p><strong>الهاشتاجات:</strong> ${data.social_plan.hashtags.join(' ')}</p>
      <p><strong>الطول الموصى به:</strong> ${data.social_plan.recommended_length}</p>
    `;

    if (data.video) {
      videoPreview.src = `http://localhost:8000/static/${data.video.split('/').pop()}`;
    }

    statusEl.textContent = 'تم إنشاء المحتوى بنجاح';
    resultsEl.classList.remove('hidden');
  } catch (error) {
    console.error(error);
    statusEl.textContent = 'حدثت مشكلة أثناء إنشاء المحتوى. تأكد من تشغيل الخادم.';
  }
});
