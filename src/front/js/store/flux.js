const getState = ({ getStore, getActions, setStore }) => {

	return {
		store: {
			people: [],
			planets: [],
			vehicles: [],
			favorites: [],
		},

		actions: {

			login: async(email, password) => {
                try {
                    let response = await fetch("https://refactored-space-xylophone-9799xjp76g47hw6r-3001.app.github.dev/api/login", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "email": email,
                            "password": password
                        })

                    })

                    const data = await response.json()
                    localStorage.setItem("token", data.access_token);
                    return true

                }   catch (error) {
                    return false
                }
            },



			getItems: () => {
				const store = getStore();
				const natures = ['people', 'planets', 'vehicles'];

				natures.forEach(async (nature) => {
					const url = `https://www.swapi.tech/api/${nature}`;

					try {
						const response = await fetch(`${url}`)
						const data = await response.json()

						data.results.forEach(async (item) => {
							const responseTwo = await fetch(`${url}/${item.uid}`)
							const dataTwo = await responseTwo.json()

							setStore({
								[nature]: [...store[nature], dataTwo.result]
							})
						})
					} 
					catch (error) {console.log(error)}
				})
			},


			addFavorite: (element) => {
				const store = getStore();
				const { favorites } = store
				const isFavorite = favorites.filter(item => item.properties.name == element.properties.name);
				console.log(favorites)

				if (isFavorite.length == 0) {
					setStore({
						favorites: [...favorites, element]
					})
				} else {
					console.log("ya existe")
				}
			},

			deleteFavorite: (element) => {
				const store = getStore();
				const { favorites } = store;
				const unFavorite = favorites.filter(item => item.properties.name != element.properties.name);

				setStore({
					favorites: unFavorite
				})
			}

		}
	}
};

export default getState;