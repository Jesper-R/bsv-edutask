describe('Req 8: Todo Management', () => {
  let uid
  let name
  let email
  let taskId

  before(function () {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user,
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
      })
    })
  })

  beforeEach(() => {
    cy.fixture('task.json').then((task) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/tasks/create',
        form: true,
        body: {
          ...task,
          userid: uid,
        },
      }).then((response) => {
        const tasks = response.body
        taskId = tasks[tasks.length - 1]._id.$oid
        cy.visit('http://localhost:3000')
        cy.reload()
        cy.get('#email').type(email)
        cy.get('form').submit()
        cy.get('.container-element a').click()
      })
    })
  })

  afterEach(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/tasks/byid/${taskId}`,
    })
  })

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`,
    })
  })

  describe('R8UC1: Adding Todo Items', () => {
    it('Valid todo item is created', () => {
      // Arrange
      cy.get('.inline-form > [type="text"]').type('successful task please')
      
      // Act
      cy.get('.inline-form').submit()

      // Assert
      cy.get('.todo-list > .todo-item').last().should('contain.text', 'successful task please')
    })
    it('Empty description makes add button disabled', () => {
      // Arrange
      // Act
      // Assert
      cy.get('.inline-form > [type="text"]').should('have.value', '')
      cy.get('.inline-form > [type="submit"').should('be.disabled')
    })
  })

  describe('R8UC2: Toggling Todo Items', () => {
    it('Toggle when previous state active', () => {
      // Arrange
      // Act
      cy.get('.todo-list > .todo-item').first().find('.checker').click()

      // Assert
      cy.get('.todo-list > .todo-item').first().find('.checker').should('have.class', 'checked')
      cy.get('.todo-list > .todo-item').first().find('.editable').should('have.css', 'text-decoration-line', 'line-through')
    })

    it('Toggle when previous state done', () => {
      // Arrange
      cy.get('.todo-list > .todo-item').first().find('.checker').click()

      // Act
      cy.get('.todo-list > .todo-item').first().find('.checker').click()

      // Assert
      cy.get('.todo-list > .todo-item').first().find('.checker').should('not.have.class', 'checked')
      cy.get('.todo-list > .todo-item').first().find('.editable').should('not.have.css', 'text-decoration-line', 'line-through')
    })
  })

  describe('R8UC3: Deleting Todo Items', () => {
    it('Delete todo item', () => {
      // Arrange
      cy.get('.todo-list > .todo-item').first().find('.editable').invoke('text').then((itemText) => {

      // Act
      cy.get('.todo-list > .todo-item').first().find('.remover').click()

      // Assert
      cy.get('.popup-inner').should('not.contain.text', itemText)
      })
    })
  })
})
