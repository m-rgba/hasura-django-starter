<script>
    import { onMount } from "svelte";
	import { Router, Route, navigate } from "svelte-routing";
	import Cookies from 'js-cookie'

	import { authToken } from './stores/auth.js'
	let refresh = Cookies.get('refresh');

	import Redirect from "./components/Redirect.svelte";

	/* Pages: User Management */
	import Home from "./pages/Home.svelte";
	import Users from "./pages/Users.svelte";
	// import Profile from "./pages/Profile.svelte";
	// import UserCreate from "./pages/UserCreate.svelte";
	// import UserEdit from "./pages/UserEdit.svelte";
	// import UserExpanded from "./pages/UserExpanded.svelte";
	/* Pages: Auth */
	import Auth from "./pages/Auth.svelte";

	/* Auth */
	let loaded = false;
	let authSuccess = false;

    onMount(() => {
		token();
	});

	function token() {		
		if ($authToken){
			console.log('Running Verify Token');
			verifyToken();
		} else if (refresh){
			console.log('Running Get New Token');
			getNewToken();
		} else {
			noToken();
		}
	}

	function noToken() {
		loaded = true;
		navigate("/login", { replace: true });
	}

	async function verifyToken() {
		const request = await fetch("http://localhost:8000/api/token/verify/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
			body: JSON.stringify({ "token" : $authToken }),
		});
		if (request.ok) {
			// Load up to homepage
			loaded = true;
			authSuccess = true;
		} else {
			// Remove old token, try to get new one
			$authToken = '';
			getNewToken();
		}
	}

	async function getNewToken() {
		const request = await fetch("http://localhost:8000/api/token/refresh/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
			body: JSON.stringify({ refresh }),
		});
		if (request.ok) {
			const response = await request.json();
			if (response.access){
				// Load up new token > go home
				$authToken = response.access;
				authSuccess = true;
				loaded = true;
			} else {
				// Clear everything > go to login
				$authToken = '';
				Cookies.set('refresh', '', { sameSite: 'strict' })
				loaded = true;
			}
		} else {
			// Clear everything > go to login
			$authToken = '';
			Cookies.set('refresh', '', { sameSite: 'strict' })
			loaded = true;
		}
	}

	export { token, verifyToken, getNewToken, noToken, authSuccess }
</script>

<Router>
	{#if loaded === true}
		{#if $authToken}
			<Route path="/"><Redirect to="home" /></Route>
			<Route path="home"><Home /></Route>
			<Route path="users"><Users /></Route>
			<Route path="*"><Redirect to="home" /></Route>
		{:else}
			<Route path="login"><Auth /></Route>
			<Route path="*"><Redirect to="login" /></Route>
		{/if}
	{/if}
</Router>