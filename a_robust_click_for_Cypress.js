const my_robust_click = (text, type = '*') => {
  cy.xpath(`//${type}[contains(text(),"${text}")]`).first().as('my_first_custom_id');
  cy.get('@my_first_custom_id').then(($element) => {
    if ($element.length > 0) {
      cy.wrap($element).click({ force: true });
      cy.wait(786);
      cy.xpath(`//${type}[contains(text(),"${text}")]`).then(($element) => {
        if ($element.length > 0) {
          cy.wrap($element).click({ multiple: true, force: true });
        }
      });
    } else {
      cy.log('Element not found');
    }
  });
};
