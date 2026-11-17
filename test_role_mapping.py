import pathlib

html = pathlib.Path('index.html').read_text(encoding='utf-8')

def test_role_labels_and_permissions_exist():
    assert 'comprador' in html
    assert 'externo' in html
    assert 'profile.role !== \'admin\'' in html
    assert 'profile.role === \'admin\'' in html
    assert 'getRoleLabel' in html


def test_external_can_only_see_orders_originated_from_own_solped():
    # El perfil externo solo debe ver OCs relacionadas con SOLPEDs que fueron emitidas
    # por su usuario y no todas las OCs del sistema.
    assert 'currentUser?.role === \'externo\'' in html
    assert 'req && req.usuario !== currentUser.username' in html
    assert 'let req = getReq(o.reqId)' in html


def test_material_master_and_keyboard_filter_support_stock_limits():
    # Requisito nuevo para el maestro de materiales y para la navegación del autocomplete.
    assert 'stock_minimo' in html
    assert 'stock_maximo' in html
    assert 'ArrowDown' in html or 'ArrowUp' in html or 'key===' in html
    assert 'autocomplete_' in html


def test_material_master_has_edit_action():
    assert 'editMat(' in html or 'openEditMat' in html or 'editarMaterial' in html


def test_alert_popups_support_close_and_escape():
    assert 'Escape' in html or 'key === \'Escape\'' in html
    assert 'closeModal()' in html or 'cerrar' in html.lower()


def test_panol_stock_view_supports_saved_position_column():
    assert 'Posición de Guardado' in html
    assert 'guardarPosicionPanol' in html


def test_quote_materials_support_individual_vat_and_oc_calculation():
    assert 'cot_item_iva_' in html
    assert '10,5%' in html
    assert 'itemIva' in html
    assert 'ivaItems' in html
    assert "req.justificacion.trim() !== '111'" in html


def test_comparative_matrix_displays_item_vat_and_print_total_uses_it():
    assert 'getCotizacionItemIva' in html
    assert 'IVA ${formatIvaLabel' in html
    assert 'ivaItemsProv' in html
    assert 'totalIvaPicking += ivaItemsProv' in html


def test_solped_table_displays_associated_purchase_order_status():
    assert 'getSolpedOcStatusHtml' in html
    assert 'o.reqId === solpedId' in html
    assert 'Estado SOLPE / OC' in html
    assert 'SOLPE: ${s.estado}' in html


def test_stock_is_synchronized_with_material_master():
    assert 'syncStockWithMaterials' in html
    assert "stockItem.id = material.id" in html
    assert "cant: 0" in html
    assert "if(syncStockWithMaterials()) saveState();" in html


def test_user_attribution_fields_exist_for_print_and_histories():
    # Smoke check across generated templates and audit fields
    assert 'usuario' in html.lower() or 'usuarioCarga' in html.lower()
    assert 'createdBy' in html or 'usuario_carga' in html or 'usuario' in html.lower()


def test_dashboard_shows_internal_and_external_lead_times():
    assert 'LEAD TIME INTERNO' in html
    assert 'LEAD TIME EXTERNO' in html
    assert 'fecha_emision' in html
    assert 'fecha_recepcion_final' in html
    assert 'getAverageDays' in html


def test_supplier_master_displays_otif_after_payment_condition():
    assert '<th>Cond. Pago</th><th>OTIF</th>' in html
    assert 'getProviderOtif' in html
    assert 'exactQuantities' in html


def test_movement_122_tracks_supplier_returns_and_adjusts_stock():
    assert 'movimientos122' in html
    assert 'window.saveDevolucion122' in html
    assert 'Movimiento 122 contabilizado' in html
    assert 'stockItem.cant' in html


def test_all_system_tables_support_dragged_column_reordering():
    assert 'document.querySelectorAll("table")' in html
    assert 'ondragstart' in html
    assert 'ondrop' in html
    assert 'reorderTableColumns' in html


def test_panol_search_is_enlarged_without_inventory_label():
    assert 'id="panolSearch"' in html
    assert 'width:min(520px, 60%)' in html
    assert 'Inventario valorizado' not in html


def test_machinery_codes_are_unique_and_auto_generated_without_collisions():
    assert 'genUniqueCode(\'EQP\', state.maquinarias, machine => machine.codigo)' in html
    assert "item.id !== id && String(item.codigo || '').trim().toUpperCase() === codigo" in html
    assert 'Código único / identificación' in html


def test_machine_and_material_masters_offer_printable_qr_labels():
    assert 'cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js' in html
    assert 'openQrLabel(\'machine\'' in html
    assert 'openQrLabel(\'material\'' in html
    assert 'window.printQrLabel' in html
    assert 'COLDLAND · ${typeLabel}' in html


def test_qr_codes_encode_direct_links_to_stock_or_machine_inventory():
    assert 'function getQrDeepLink(type, id)' in html
    assert 'text: getQrDeepLink(type, record.id)' in html
    assert "pendingQrMaterialId = qrTarget.id" in html
    assert "navTo('panol')" in html
    assert "selectedInventoryMachineId = qrTarget.id" in html
    assert "navTo('inventario')" in html
    assert 'Despiece BOM · ${selectedMachine.codigo}' in html
