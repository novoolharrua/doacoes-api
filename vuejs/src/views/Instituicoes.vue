<template>
	<div class="container">
		<b-alert show dismissible v-for="mensagem in mensagens"
			:key="mensagem.texto"
			:variant="mensagem.tipo">{{ mensagem.texto }}</b-alert>
		<b-card>
			<b-form-group label="Nome:">
				<b-form-input type="text" size="lg"
					v-model="institution.name"
					placeholder="Informe o Nome"></b-form-input>
			</b-form-group>
			<b-form-group label="Endereço:">
				<b-form-input type="text" size="lg"
					v-model="institution.address"
					placeholder="Informe o Endereço"></b-form-input>
			</b-form-group>
			<b-form-group label="E-mail:">
				<b-form-input type="email" size="lg"
					v-model="institution.email"
					placeholder="Informe o Email"></b-form-input>
			</b-form-group>
			<b-form-group label="Senha:">
				<b-form-input type="password" size="lg"
					v-model="institution.passwd"
					placeholder="Informe sua senha"></b-form-input>
			</b-form-group >
				<b-form-group label="Tipos de Doações:">
				<b-form-checkbox-group id="checkbox-group-2" v-model="institution.types" name="flavour-2">
					<b-form-checkbox value="FOOD">Alimentação</b-form-checkbox>
					<b-form-checkbox value="CLOTHING">Roupas</b-form-checkbox>
					<b-form-checkbox value="RELIGION">Religião</b-form-checkbox>
					<b-form-checkbox value="OTHERS">Outros</b-form-checkbox>
				</b-form-checkbox-group>
				</b-form-group>
			<hr>
			<b-button @click="salvar"
				size="lg" variant="primary">Salvar</b-button>
			<b-button @click="obterInstitutions"
				size="lg" variant="success"
				class="ml-2">Obter Instituições</b-button>
		</b-card>
		<hr>
		<b-list-group>
			<b-list-group-item v-for="(instituicao, id) in Institutions" :key="id">
				<strong>Nome: </strong> {{ instituicao.name }}<br>
				<strong>Endereço: </strong> {{ instituicao.address }}<br>
				<strong>E-mail: </strong> {{ instituicao.email }}<br>
				<strong>Tipos de Doações: </strong> {{ instituicao.types }}<br>

				<b-button variant="warning" size="lg"
					@click="carregar(instituicao.id)">Carregar</b-button>
				<b-button variant="danger" size="lg" class="ml-2"
					@click="excluir(instituicao.id)">Excluir</b-button>
			</b-list-group-item>
		</b-list-group>
	</div>
</template>
<script>
export default {
	data() {
		return {
			mensagens: [],
			Institutions: [],
			id: null,
			institution: {
      			name: '',
      			address: '',
				email: '',
				passwd:'',
				types: '',
				shelter:0
			}
		}
	},
	methods: {
		limpar() {
			this.name = '',
      		this.address = '',
			this.email = '',
			this.passwd ='',
			this.types = '',
			this.shelter = 0
			this.id = null
			this.mensagens = []
		},
		carregar(id_instituition) {
			this.id = id
			this.institution = { ...this.Institutions[id] }
		},
		excluir(id_instituition) {
			this.$http.delete(`/institution/${id_instituition}`)
				.then(() => {
					this.limpar()
					this.obterInstitutions()
					})
				.catch(err => {
					this.limpar()
					this.mensagens.push({
						texto: 'Problema para excluir!',
						tipo: 'danger'
					})
				})
		},
		salvar() {
			this.institution.types = this.institution.types.join(",")
			
			const metodo = 'post'
			this.$http[metodo](`/institution`, this.institution)
				.then(() => {
					this.limpar()
					this.obterInstitutions()
					this.mensagens.push({
						texto: 'Operação realizada com sucesso!',
						tipo: 'success'
					})
				})
		},
		obterInstitutions() {
			this.$http.get('institution').then(res => {
				console.log(res.data)
				this.Institutions = res.data
			})
		}
	}
}
</script>

<style>
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
	font-size: 1.5rem;
}

#app h1 {
	text-align: center;
	margin: 50px;
}
</style>
