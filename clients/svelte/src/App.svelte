<script>
    import { onMount } from "svelte";
	import { Router, Route } from "svelte-routing";
	import { authLoaded } from './stores/auth.js'
	import { token } from './shared/auth.js'

	import Redirect from "./components/Redirect.svelte";

	/* Pages: User Management */
	import Home from "./pages/Home.svelte";
	import Users from "./pages/Users.svelte";
	import UserExpanded from "./pages/UserExpanded.svelte";
	import UserCreate from "./pages/UserCreate.svelte";
	import Profile from "./pages/Profile.svelte";
	/* Pages: Auth */
	import Auth from "./pages/Auth.svelte";

    onMount(() => {
		token(false);
	});
	
	let accessToken = localStorage.getItem('token');
	console.log('> Mounted Main App')
</script>

<Router>
	{#if $authLoaded === true}
		{#if !accessToken}
			<Route path="login"><Auth /></Route>
			<Route path="*"><Redirect to="login" /></Route>
		{:else}
			<Route path="/"><Redirect to="home" /></Route>
			<Route path="home"><Home /></Route>
			<Route path="users"><Users /></Route>
			<Route path="user/create"><UserCreate /></Route>
			<Route path="user/:username" let:params><UserExpanded username="{params.username}" /></Route>
			<Route path="profile"><Profile /></Route>
			<Route path="login"><Redirect to="home" /></Route>
		{/if}
	{/if}
</Router>