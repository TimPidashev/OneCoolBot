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
          href="https://discord.gg/EDRjZdkGBG"
          target="_blank"
          class="button--green"
        >
          Discord Server
        </a>
        <a
          href="https://put_invite_link_here_when_ready"
          target="_blank"
          class="button--grey"
        >
          Invite Me!
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

.container:after{
  content:'';
  height:300px;
  width:100%;
  display:block;
  background-image:linear-gradient(90deg, rgba(252,25,154,.1) 1px, rgba(0,0,0,0) 1px), linear-gradient(0deg, rgba(252,25,154,.1) 1px, rgba(0,0,0,0) 1px);
  background-position:bottom;
  background-repeat:repeat;
  background-size:20px 20px;
  left: -25px;
  position: fixed;
  pointer-events: none;
  bottom: 0;
  transform: perspective(100px) rotateX(60deg);
  z-index: 0;
}

.container:after {
    background-image: repeating-linear-gradient(to bottom, transparent 0 ,transparent 2px, #FFF 2px, #FFF 4px);
    background-size: 100% 4px cover;
    transform-origin: 50% 50%;
    content: '';
    opacity: 0.02;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
}

.title {
  font-family: 'New_Zelek' 'Arial';
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
