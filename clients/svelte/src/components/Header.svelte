<script>
    import { onMount, onDestroy } from "svelte";
    import { link } from "svelte-routing";
    import { authLoaded } from '../stores/auth.js'
    import { token } from '../shared/auth.js'

    import Cookies from 'js-cookie'

    export let headerType;

    onMount(() => {
        if(headerType === 'auth'){
            token(false);
        } else {
            token();
        }
    });

    let currentLocation = window.location.pathname;

    function logout() {
        Cookies.set('refresh', "", { sameSite: 'strict' });
        localStorage.setItem("token", "");
        localStorage.setItem("user_name", "");
        localStorage.setItem("user_email", "");
        localStorage.setItem("user_role", "");
        location.replace("/");
    }
</script>

{#if headerType === 'auth'}
    <header style="justify-content:center;">
        <div class="nav logo"><img alt="Logo" src="/logo-light.svg" /></div>
    </header>
{:else}
    <header>
        <div class="nav logo"><img alt="Logo" src="/logo-light.svg" /></div>
        <div class="nav {currentLocation === '/home' ? "active": "inactive"}"><a use:link href="/">Home</a></div>
        <div style="margin-left:auto;" class=" {currentLocation === '/users' ? "active": "inactive"} nav"><a use:link href="/users">Users</a></div>
        <div class="nav {currentLocation === '/profile' ? "active": "inactive"}"><a use:link href="/profile">Profile</a></div>
        <div class="nav"><a on:click="{logout}" href="#!">Logout</a></div>
    </header>
{/if}