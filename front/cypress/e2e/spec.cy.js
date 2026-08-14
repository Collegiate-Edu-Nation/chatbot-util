// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

describe('Interrupt Generation Progress', () => {
  it('passes', () => {
    cy.visit('/')
    cy.get('button').contains('Generate').click()
    cy.contains('Interrupt').click()
    cy.get('button').contains('Generate')
  })
})
