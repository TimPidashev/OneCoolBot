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
  background-color: transparent !important;
  background-image: linear-gradient(to bottom, #200933 75%, #3d0b43);
  background-size: auto 100vh;
  background-position: top;
  background-repeat: no-repeat;
  position: relative;
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.container::after{
  content:'';
  height:300px;
  width:100%;
  display:block;
  background-image:linear-gradient(90deg, rgba(252,25,154,.1) 1px, rgba(0,0,0,0) 1px), linear-gradient(0deg, rgba(252,25,154,.1) 1px, rgba(0,0,0,0) 1px);
  background-position:bottom;
  background-repeat:repeat;
  background-size:20px 20px;
  left: -25px;
  position: absolute;
  pointer-events: none;
  bottom: 0;
  transform: perspective(100px) rotateX(60deg);
  z-index: 0;
  overflow: hidden;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #9B59B6;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #3d0b43;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

</style>
