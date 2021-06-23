<template>
  <div class="container">
    <div>
      <logo />
      <h1 class="title">
        OneCoolBot
      </h1>
      <h2 class="subtitle">
        An advanced and extremely capable cyberpunk discord bot that's out of this world! 
      </h2>
      <div class="links">
        <a
          href="https://nuxtjs.org/"
          target="_blank"
          class="button--green"
        >
          Documentation
        </a>
        <a
          href="https://github.com/nuxt/nuxt.js"
          target="_blank"
          class="button--grey"
        >
          GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  background-image: url("data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='41px' height='40px' viewBox='0 0 41 40' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Cdefs%3E%3ClinearGradient x1='50%25' y1='0%25' x2='50%25' y2='97.6652818%25' id='linearGradient-1'%3E%3Cstop stop-color='%23FC28A8' offset='0%25'%3E%3C/stop%3E%3Cstop stop-color='%2303EDF9' offset='100%25'%3E%3C/stop%3E%3C/linearGradient%3E%3C/defs%3E%3Cg id='Page-1' stroke='none' stroke-width='1' fill='none' fill-rule='evenodd'%3E%3Cg id='letterpress-dark' fill='url(%23linearGradient-1)'%3E%3Cg id='Group'%3E%3Cpath d='M30.2354,39.8836 C29.9195,39.8862 29.6057,39.8287 29.3109,39.7139 C28.9896,39.5885 28.6977,39.3979 28.4539,39.1539 L12.6999,24.7799 L9.23917,27.4037 L5.83434,29.986 C5.70454,30.0845 5.56201,30.1626 5.41164,30.2189 C5.20259,30.2976 4.9783,30.3339 4.7519,30.3239 C4.36361,30.3068 3.99356,30.1543 3.70588,29.8929 L1.50588,27.8929 C1.33452,27.7368 1.19763,27.5466 1.10396,27.3346 C1.01029,27.1225 0.961914,26.8933 0.961914,26.6614 C0.961914,26.4296 1.01029,26.2004 1.10396,25.9883 C1.19763,25.7762 1.33452,25.5861 1.50588,25.4299 L7.45788,19.9999 L4.67072,17.4532 L1.50734,14.5689 C1.33584,14.4129 1.19883,14.2227 1.10507,14.0107 C1.01132,13.7986 0.962891,13.5693 0.962891,13.3374 C0.962891,13.1056 1.01132,12.8763 1.10507,12.6642 C1.19883,12.4521 1.33584,12.262 1.50734,12.1059 L3.70734,10.1059 C3.72926,10.086 3.75165,10.0667 3.7745,10.048 C4.05213,9.82027 4.39666,9.68789 4.7569,9.67196 C5.14519,9.65479 5.52725,9.77401 5.83688,10.0089 L12.6999,15.2179 L28.4519,0.843942 C28.5452,0.751682 28.6455,0.666763 28.7519,0.589942 C29.1153,0.325601 29.5436,0.164633 29.9911,0.124137 C30.0919,0.11502 30.1928,0.112086 30.2933,0.115234 C30.6444,0.123748 30.9918,0.206443 31.3117,0.360027 L39.5477,4.32103 C39.9716,4.52522 40.3292,4.84487 40.5795,5.24325 C40.7787,5.56023 40.9035,5.9168 40.9462,6.28629 C40.9574,6.38148 40.9632,6.47754 40.9633,6.57401 L40.9633,6.67295 C40.9633,6.65781 40.9631,6.64268 40.9627,6.62757 L40.9627,33.3704 C40.9631,33.3552 40.9633,33.3401 40.9633,33.3249 L40.9633,33.4199 C40.9633,33.5146 40.9579,33.609 40.9472,33.7025 C40.9055,34.0754 40.7802,34.4355 40.5793,34.7552 C40.329,35.1534 39.9714,35.4729 39.5477,35.677 L31.3117,39.638 C31.0191,39.7785 30.7037,39.8596 30.3833,39.879 C30.3341,39.882 30.2848,39.8835 30.2354,39.8836 Z M30.9509,10.9369 L19.0028,19.9987 L30.9549,29.0639 L30.9509,10.9369 Z' id='Shape'%3E%3C/path%3E%3C/g%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  position: relative;
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

</style>
