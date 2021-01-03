<script>
  import { navigate } from "svelte-routing";
  import { authToken } from '../stores/auth.js'
  import Cookies from 'js-cookie'

  export let headerType;

  function logout() {
    $authToken = null;
    Cookies.set('refresh', null);
    navigate("/login", { replace: true });
  }
</script>

<style>
</style>

{#if headerType === 'auth'}
  <header style="justify-content:center;">
    <div class="nav logo"><img alt="Logo" src="/logo-light.svg" /></div>
  </header>
{:else}
  <header>
    <div class="nav logo"><img alt="Logo" src="/logo-light.svg" /></div>
    <div class="nav"><a href="/">Home</a></div>
    <div style="margin-left:auto;" class="nav"><a href="/users">Users</a></div>
    <div class="nav"><a href="#!">Profile</a></div>
    <div class="nav"><a on:click="{logout}" href="#!">Logout</a></div>
  </header>
{/if}