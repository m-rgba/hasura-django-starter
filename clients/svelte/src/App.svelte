<script>
    import { onMount } from "svelte";
	import { Router, Route } from "svelte-routing";
	import { authLoaded } from './stores/auth.js'
	import { token } from './shared/auth.js'
    import { gqlResponseHandler } from './shared/requests.js'

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
		updateLastLoginDate();
	});

	let accessToken = localStorage.getItem('token');

    async function updateLastLoginDate() {
        let username = localStorage.getItem('user_name');
		if ( username ){
			const variable = {};
			const query = `
				mutation updateProfileEmail($username: String!, $lastLogin: timestamptz!) {
					update_auth_user(where: {username: {_eq: $username}}, _set: {last_login: $lastLogin}) {
						returning {
							username
						}
					}
				}
			`;
			variable["lastLogin"] = new Date().toISOString();
            variable["username"] = username;
            const accessToken = await token();
			const request = await fetch("http://localhost:8080/v1/graphql", {
				method: "POST",
				headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
				body: JSON.stringify({ query: query, variables: variable })
			});
			const updateLastLogin = await gqlResponseHandler(request);
			if (updateLastLogin.success === true){
                // console.log('> Last login > Updated');
			} else {
				// console.log('> Last login > Failed');
			}
		} else {
            // console.log('> Last login > Cancelled');
        }
    };

	// console.log('> Mounted Main App')
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