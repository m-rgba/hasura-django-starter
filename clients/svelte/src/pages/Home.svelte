<script>
    import { onMount } from "svelte";
    import { authToken } from '../stores/auth.js'
    
    import Cookies from 'js-cookie'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {
        console.log($authToken);
		console.log(Cookies.get('refresh'));
	});
</script>

<Header />

<content>
    <div class="container pt-xl mb-xl">
        <div class="row">
            <div class="col-12 mb-sm">
                <h1>Home</h1>
            </div>
            <div class="col-12">
                <p class="muted">[ Placeholder for your content ]</p>
            </div>
        </div>
    </div>
</content>

<Footer />