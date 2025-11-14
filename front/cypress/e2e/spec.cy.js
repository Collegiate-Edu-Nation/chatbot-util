describe('Interrupt Generation Progress', () => {
  it('passes', () => {
    cy.visit('http://localhost:5173')
    cy.get('button').contains('Generate').click()
    cy.contains('Interrupt').click()
    cy.get('button').contains('Generate')
  })
})
