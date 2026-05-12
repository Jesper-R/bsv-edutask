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
    it('Empty description makes add button disabled', () => {
      // Arrange
      // Act
      // Assert
    })
    it('Valid todo item is created', () => {
      // s
    })
  })
})
