// ComicCraft Frontend Interactions

document.addEventListener('DOMContentLoaded', () => {
  // Preset Templates
  const presets = {
    fox: {
      prompt: "A brave fox explores an enchanted forest to find the legendary whispering crystal.",
      character: "Free",
      setting: "Enchanted Forest",
      tone: "Dramatic",
      style: "Comic Book"
    },
    cyberpunk: {
      prompt: "A cyber-augmented detective investigates an anomaly in the high-tech neon underworld.",
      character: "Kaelen",
      setting: "Futuristic Megacity",
      tone: "Action-packed",
      style: "Cyberpunk"
    },
    space: {
      prompt: "An interstellar cartographer uncovers a forgotten alien monolith orbiting a dying star.",
      character: "Nova",
      setting: "Deep Space Station",
      tone: "Poetic",
      style: "Sci-Fi"
    },
    funny: {
      prompt: "A clumsy apprentice wizard accidentally turns the academy headmaster's hat into a mischievous duck.",
      character: "Barnaby",
      setting: "Magic Academy",
      tone: "Funny",
      style: "Anime"
    }
  };

  // Wire Preset Chips
  document.querySelectorAll('.preset-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const key = chip.getAttribute('data-preset');
      const data = presets[key];
      if (data) {
        const promptInput = document.getElementById('story-prompt');
        const charInput = document.getElementById('character-name');
        const settingInput = document.getElementById('setting-input');
        const toneInput = document.getElementById('story-tone');
        const styleInput = document.getElementById('art-style');

        if (promptInput) promptInput.value = data.prompt;
        if (charInput) charInput.value = data.character;
        if (settingInput) settingInput.value = data.setting;
        if (toneInput) toneInput.value = data.tone;
        if (styleInput) styleInput.value = data.style;

        // Visual flash highlight
        chip.style.transform = 'scale(1.1)';
        setTimeout(() => chip.style.transform = '', 200);
      }
    });
  });

  // Handle Comic Generation Form Submission Loading Overlay
  const form = document.getElementById('comic-create-form');
  const overlay = document.getElementById('loading-overlay');
  const boomText = document.getElementById('comic-boom-text');
  const subText = document.getElementById('loading-sub-text');

  if (form && overlay) {
    form.addEventListener('submit', () => {
      overlay.style.display = 'flex';

      const soundEffects = ['KABOOM!', 'ZAP!', 'WHAM!', 'POW!', 'SHAZAM!'];
      const steps = [
        'Outlining 5-panel arc with Gemini Flash...',
        'Writing dialogues & captions with Gemini Pro...',
        'Inking illustrations with Stable Diffusion...',
        'Assembling layout and binding pages...',
        'Polishing PDF comic strip...'
      ];

      let idx = 0;
      setInterval(() => {
        idx = (idx + 1) % soundEffects.length;
        if (boomText) boomText.textContent = soundEffects[idx];
        if (subText) subText.textContent = steps[idx];
      }, 2200);
    });
  }
});
