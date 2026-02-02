#!/usr/bin/env python3
"""
Test EDI XML Messages - Real-world AS2 data exchange
Sends realistic EDI XML documents (Purchase Orders, Invoices, etc.)
Run: docker exec p1-as2 python3 /app/unittest/test_edi_xml_messages.py
"""
import os
import sys
import time
from datetime import datetime

# Set up Django environment
os.chdir('/app/P1')
sys.path.insert(0, '/app/P1')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

from django.core.management import call_command
from pyas2.models import Partner, Message, Organization

# Sample EDI XML Documents
EDI_PURCHASE_ORDER = """<?xml version="1.0" encoding="UTF-8"?>
<PurchaseOrder xmlns="http://www.example.com/EDI/PO" version="1.0">
  <Header>
    <PONumber>PO-2026-001234</PONumber>
    <PODate>2026-02-01</PODate>
    <BuyerID>BUYER-12345</BuyerID>
    <SellerID>SELLER-67890</SellerID>
    <Currency>USD</Currency>
    <PaymentTerms>Net 30</PaymentTerms>
    <ShipmentTerms>FOB Destination</ShipmentTerms>
  </Header>
  <BuyerInfo>
    <Name>Acme Corporation</Name>
    <Address>
      <Street>123 Business Ave</Street>
      <City>New York</City>
      <State>NY</State>
      <ZipCode>10001</ZipCode>
      <Country>USA</Country>
    </Address>
    <Contact>
      <Name>John Smith</Name>
      <Phone>+1-212-555-0100</Phone>
      <Email>john.smith@acme.com</Email>
    </Contact>
  </BuyerInfo>
  <SellerInfo>
    <Name>Global Supplies Inc</Name>
    <Address>
      <Street>456 Commerce Blvd</Street>
      <City>Los Angeles</City>
      <State>CA</State>
      <ZipCode>90001</ZipCode>
      <Country>USA</Country>
    </Address>
    <Contact>
      <Name>Jane Doe</Name>
      <Phone>+1-310-555-0200</Phone>
      <Email>jane.doe@globalsupplies.com</Email>
    </Contact>
  </SellerInfo>
  <ShippingAddress>
    <Name>Acme Warehouse</Name>
    <Street>789 Distribution Way</Street>
    <City>Chicago</City>
    <State>IL</State>
    <ZipCode>60601</ZipCode>
    <Country>USA</Country>
  </ShippingAddress>
  <LineItems>
    <LineItem>
      <LineNumber>1</LineNumber>
      <ProductCode>WIDGET-001</ProductCode>
      <Description>Premium Widget - Blue</Description>
      <Quantity>100</Quantity>
      <UnitOfMeasure>EA</UnitOfMeasure>
      <UnitPrice>25.50</UnitPrice>
      <TotalPrice>2550.00</TotalPrice>
      <RequestedDeliveryDate>2026-02-15</RequestedDeliveryDate>
    </LineItem>
    <LineItem>
      <LineNumber>2</LineNumber>
      <ProductCode>GADGET-002</ProductCode>
      <Description>Advanced Gadget - Red</Description>
      <Quantity>50</Quantity>
      <UnitOfMeasure>EA</UnitOfMeasure>
      <UnitPrice>45.75</UnitPrice>
      <TotalPrice>2287.50</TotalPrice>
      <RequestedDeliveryDate>2026-02-15</RequestedDeliveryDate>
    </LineItem>
    <LineItem>
      <LineNumber>3</LineNumber>
      <ProductCode>TOOL-003</ProductCode>
      <Description>Professional Tool Kit</Description>
      <Quantity>25</Quantity>
      <UnitOfMeasure>SET</UnitOfMeasure>
      <UnitPrice>125.00</UnitPrice>
      <TotalPrice>3125.00</TotalPrice>
      <RequestedDeliveryDate>2026-02-20</RequestedDeliveryDate>
    </LineItem>
  </LineItems>
  <Summary>
    <SubTotal>7962.50</SubTotal>
    <Tax>637.00</Tax>
    <Shipping>150.00</Shipping>
    <Total>8749.50</Total>
  </Summary>
  <Notes>
    <Note>Please confirm receipt of this purchase order within 24 hours.</Note>
    <Note>All items must be shipped together.</Note>
    <Note>Include packing slip with shipment.</Note>
  </Notes>
</PurchaseOrder>"""

EDI_INVOICE = """<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="http://www.example.com/EDI/Invoice" version="1.0">
  <Header>
    <InvoiceNumber>INV-2026-005678</InvoiceNumber>
    <InvoiceDate>2026-02-01</InvoiceDate>
    <DueDate>2026-03-03</DueDate>
    <POReference>PO-2026-001234</POReference>
    <SellerID>SELLER-67890</SellerID>
    <BuyerID>BUYER-12345</BuyerID>
    <Currency>USD</Currency>
    <PaymentTerms>Net 30</PaymentTerms>
  </Header>
  <SellerInfo>
    <Name>Global Supplies Inc</Name>
    <TaxID>12-3456789</TaxID>
    <Address>
      <Street>456 Commerce Blvd</Street>
      <City>Los Angeles</City>
      <State>CA</State>
      <ZipCode>90001</ZipCode>
      <Country>USA</Country>
    </Address>
    <BankInfo>
      <BankName>First National Bank</BankName>
      <AccountNumber>****1234</AccountNumber>
      <RoutingNumber>123456789</RoutingNumber>
    </BankInfo>
  </SellerInfo>
  <BuyerInfo>
    <Name>Acme Corporation</Name>
    <TaxID>98-7654321</TaxID>
    <Address>
      <Street>123 Business Ave</Street>
      <City>New York</City>
      <State>NY</State>
      <ZipCode>10001</ZipCode>
      <Country>USA</Country>
    </Address>
  </BuyerInfo>
  <LineItems>
    <LineItem>
      <LineNumber>1</LineNumber>
      <ProductCode>WIDGET-001</ProductCode>
      <Description>Premium Widget - Blue</Description>
      <Quantity>100</Quantity>
      <UnitPrice>25.50</UnitPrice>
      <TotalPrice>2550.00</TotalPrice>
    </LineItem>
    <LineItem>
      <LineNumber>2</LineNumber>
      <ProductCode>GADGET-002</ProductCode>
      <Description>Advanced Gadget - Red</Description>
      <Quantity>50</Quantity>
      <UnitPrice>45.75</UnitPrice>
      <TotalPrice>2287.50</TotalPrice>
    </LineItem>
    <LineItem>
      <LineNumber>3</LineNumber>
      <ProductCode>TOOL-003</ProductCode>
      <Description>Professional Tool Kit</Description>
      <Quantity>25</Quantity>
      <UnitPrice>125.00</UnitPrice>
      <TotalPrice>3125.00</TotalPrice>
    </LineItem>
  </LineItems>
  <Summary>
    <SubTotal>7962.50</SubTotal>
    <TaxRate>8.00</TaxRate>
    <TaxAmount>637.00</TaxAmount>
    <ShippingCost>150.00</ShippingCost>
    <TotalAmount>8749.50</TotalAmount>
  </Summary>
  <PaymentInstructions>
    <Method>Wire Transfer</Method>
    <BankName>First National Bank</BankName>
    <AccountNumber>****1234</AccountNumber>
    <RoutingNumber>123456789</RoutingNumber>
    <Reference>INV-2026-005678</Reference>
  </PaymentInstructions>
</Invoice>"""

EDI_SHIPMENT_NOTICE = """<?xml version="1.0" encoding="UTF-8"?>
<ShipmentNotice xmlns="http://www.example.com/EDI/ASN" version="1.0">
  <Header>
    <ASNNumber>ASN-2026-009876</ASNNumber>
    <ASNDate>2026-02-01T14:30:00Z</ASNDate>
    <POReference>PO-2026-001234</POReference>
    <ShipperID>SELLER-67890</ShipperID>
    <ConsigneeID>BUYER-12345</ConsigneeID>
    <CarrierName>FastShip Logistics</CarrierName>
    <TrackingNumber>1Z999AA10123456784</TrackingNumber>
    <EstimatedDelivery>2026-02-05</EstimatedDelivery>
  </Header>
  <ShipFrom>
    <Name>Global Supplies Warehouse</Name>
    <Address>
      <Street>789 Warehouse Rd</Street>
      <City>Los Angeles</City>
      <State>CA</State>
      <ZipCode>90002</ZipCode>
      <Country>USA</Country>
    </Address>
  </ShipFrom>
  <ShipTo>
    <Name>Acme Warehouse</Name>
    <Address>
      <Street>789 Distribution Way</Street>
      <City>Chicago</City>
      <State>IL</State>
      <ZipCode>60601</ZipCode>
      <Country>USA</Country>
    </Address>
  </ShipTo>
  <Packages>
    <Package>
      <PackageNumber>1</PackageNumber>
      <TrackingNumber>1Z999AA10123456784</TrackingNumber>
      <Weight>45.5</Weight>
      <WeightUnit>LBS</WeightUnit>
      <Dimensions>
        <Length>24</Length>
        <Width>18</Width>
        <Height>12</Height>
        <Unit>IN</Unit>
      </Dimensions>
      <Contents>
        <Item>
          <ProductCode>WIDGET-001</ProductCode>
          <Quantity>100</Quantity>
        </Item>
        <Item>
          <ProductCode>GADGET-002</ProductCode>
          <Quantity>50</Quantity>
        </Item>
      </Contents>
    </Package>
    <Package>
      <PackageNumber>2</PackageNumber>
      <TrackingNumber>1Z999AA10123456785</TrackingNumber>
      <Weight>62.3</Weight>
      <WeightUnit>LBS</WeightUnit>
      <Dimensions>
        <Length>30</Length>
        <Width>24</Width>
        <Height>18</Height>
        <Unit>IN</Unit>
      </Dimensions>
      <Contents>
        <Item>
          <ProductCode>TOOL-003</ProductCode>
          <Quantity>25</Quantity>
        </Item>
      </Contents>
    </Package>
  </Packages>
  <Summary>
    <TotalPackages>2</TotalPackages>
    <TotalWeight>107.8</TotalWeight>
    <WeightUnit>LBS</WeightUnit>
  </Summary>
</ShipmentNotice>"""

EDI_INVENTORY_REPORT = """<?xml version="1.0" encoding="UTF-8"?>
<InventoryReport xmlns="http://www.example.com/EDI/Inventory" version="1.0">
  <Header>
    <ReportID>INV-RPT-2026-001</ReportID>
    <ReportDate>2026-02-01T00:00:00Z</ReportDate>
    <WarehouseID>WH-001</WarehouseID>
    <WarehouseName>Global Supplies Main Warehouse</WarehouseName>
    <ReportType>Daily Snapshot</ReportType>
  </Header>
  <WarehouseInfo>
    <Name>Global Supplies Main Warehouse</Name>
    <Address>
      <Street>789 Warehouse Rd</Street>
      <City>Los Angeles</City>
      <State>CA</State>
      <ZipCode>90002</ZipCode>
      <Country>USA</Country>
    </Address>
    <Capacity>
      <TotalSquareFeet>50000</TotalSquareFeet>
      <UsedSquareFeet>32500</UsedSquareFeet>
      <AvailableSquareFeet>17500</AvailableSquareFeet>
    </Capacity>
  </WarehouseInfo>
  <InventoryItems>
    <Item>
      <SKU>WIDGET-001</SKU>
      <Description>Premium Widget - Blue</Description>
      <Category>Widgets</Category>
      <QuantityOnHand>1250</QuantityOnHand>
      <QuantityReserved>100</QuantityReserved>
      <QuantityAvailable>1150</QuantityAvailable>
      <ReorderPoint>500</ReorderPoint>
      <ReorderQuantity>1000</ReorderQuantity>
      <UnitCost>18.50</UnitCost>
      <Location>A-12-03</Location>
    </Item>
    <Item>
      <SKU>GADGET-002</SKU>
      <Description>Advanced Gadget - Red</Description>
      <Category>Gadgets</Category>
      <QuantityOnHand>875</QuantityOnHand>
      <QuantityReserved>50</QuantityReserved>
      <QuantityAvailable>825</QuantityAvailable>
      <ReorderPoint>300</ReorderPoint>
      <ReorderQuantity>500</ReorderQuantity>
      <UnitCost>32.25</UnitCost>
      <Location>B-08-15</Location>
    </Item>
    <Item>
      <SKU>TOOL-003</SKU>
      <Description>Professional Tool Kit</Description>
      <Category>Tools</Category>
      <QuantityOnHand>450</QuantityOnHand>
      <QuantityReserved>25</QuantityReserved>
      <QuantityAvailable>425</QuantityAvailable>
      <ReorderPoint>150</ReorderPoint>
      <ReorderQuantity>200</ReorderQuantity>
      <UnitCost>89.00</UnitCost>
      <Location>C-15-22</Location>
    </Item>
    <Item>
      <SKU>PART-004</SKU>
      <Description>Replacement Part Assembly</Description>
      <Category>Parts</Category>
      <QuantityOnHand>2340</QuantityOnHand>
      <QuantityReserved>0</QuantityReserved>
      <QuantityAvailable>2340</QuantityAvailable>
      <ReorderPoint>1000</ReorderPoint>
      <ReorderQuantity>2000</ReorderQuantity>
      <UnitCost>5.75</UnitCost>
      <Location>D-03-08</Location>
    </Item>
  </InventoryItems>
  <Summary>
    <TotalSKUs>4</TotalSKUs>
    <TotalQuantityOnHand>4915</TotalQuantityOnHand>
    <TotalQuantityReserved>175</TotalQuantityReserved>
    <TotalQuantityAvailable>4740</TotalQuantityAvailable>
    <TotalInventoryValue>156842.50</TotalInventoryValue>
  </Summary>
</InventoryReport>"""

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_step(step, text):
    print(f"[Step {step}] {text}")

def print_success(text):
    print(f"  ✓ {text}")

def print_error(text):
    print(f"  ✗ {text}")

def print_info(text):
    print(f"  → {text}")

def send_edi_message(partner, doc_type, content, test_num):
    """Send an EDI XML message"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"EDI_{doc_type}_{timestamp}_{test_num}.xml"
    
    try:
        # Save to file
        filepath = f'/app/P1/data/{filename}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_info(f"Sending: {filename} ({len(content)} bytes)")
        
        # Get organization
        org = Organization.objects.first()
        
        # Send using management command
        call_command('sendas2message',
                   org.as2_name,
                   partner.as2_name,
                   filepath,
                   delete=True)
        
        print_success(f"{doc_type} sent successfully")
        return True
        
    except Exception as e:
        print_error(f"{doc_type} failed: {e}")
        return False

def main():
    print_header("EDI XML AS2 Message Exchange Test")
    print("Testing real-world EDI documents with AS2 protocol")
    print()
    
    # Get initial counts
    print_step(1, "Getting initial message counts...")
    initial_count = Message.objects.count()
    initial_out = Message.objects.filter(direction='OUT').count()
    initial_in = Message.objects.filter(direction='IN').count()
    
    print_info(f"Total messages: {initial_count}")
    print_info(f"Outbound: {initial_out}")
    print_info(f"Inbound: {initial_in}")
    print()
    
    # Check partner
    print_step(2, "Checking partner configuration...")
    partners = Partner.objects.all()
    if not partners.exists():
        print_error("No partners configured!")
        return False
    
    partner = partners.first()
    print_success(f"Using partner: {partner.as2_name}")
    print()
    
    # Send EDI documents
    print_step(3, "Sending EDI XML documents...")
    print()
    
    documents = [
        ("Purchase_Order", EDI_PURCHASE_ORDER),
        ("Invoice", EDI_INVOICE),
        ("Shipment_Notice", EDI_SHIPMENT_NOTICE),
        ("Inventory_Report", EDI_INVENTORY_REPORT),
    ]
    
    success_count = 0
    for i, (doc_type, content) in enumerate(documents, 1):
        print(f"  [{i}/{len(documents)}] {doc_type}")
        if send_edi_message(partner, doc_type, content, i):
            success_count += 1
        time.sleep(2)  # Delay between messages
        print()
    
    print("-" * 80)
    print(f"Results: {success_count}/{len(documents)} EDI documents sent")
    print()
    
    # Wait for processing
    print_step(4, "Waiting for messages to be processed...")
    time.sleep(3)
    print()
    
    # Get final counts
    print_step(5, "Checking final message counts...")
    final_count = Message.objects.count()
    final_out = Message.objects.filter(direction='OUT').count()
    final_in = Message.objects.filter(direction='IN').count()
    
    print_info(f"Total messages: {final_count} (+{final_count - initial_count})")
    print_info(f"Outbound: {final_out} (+{final_out - initial_out})")
    print_info(f"Inbound: {final_in} (+{final_in - initial_in})")
    print()
    
    # Show recent messages
    print_step(6, "Recent messages...")
    recent = Message.objects.all().order_by('-timestamp')[:10]
    for msg in recent:
        status_icon = "✓" if msg.status == 'S' else "✗" if msg.status == 'E' else "⋯"
        direction = "OUT" if msg.direction == 'OUT' else "IN "
        print(f"  {status_icon} [{direction}] {msg.message_id[:50]}... | {msg.timestamp}")
    print()
    
    # Summary
    print_header("Test Summary")
    
    results = [
        ("Partner configured", partner is not None),
        ("EDI documents sent", success_count > 0),
        ("Message count increased", final_count > initial_count),
        ("All documents successful", success_count == len(documents))
    ]
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print_success("ALL TESTS PASSED!")
        print()
        print("EDI Document Sizes:")
        print(f"  - Purchase Order: {len(EDI_PURCHASE_ORDER)} bytes")
        print(f"  - Invoice: {len(EDI_INVOICE)} bytes")
        print(f"  - Shipment Notice: {len(EDI_SHIPMENT_NOTICE)} bytes")
        print(f"  - Inventory Report: {len(EDI_INVENTORY_REPORT)} bytes")
        print()
        print("Verify in your browser:")
        print("  - Dashboard: http://192.168.1.200:8001/")
        print("  - Messages: http://192.168.1.200:8001/messages")
        print("  - Admin: http://192.168.1.200:8001/admin/pyas2/message/")
        print()
        print("Click the eye icon (👁️) to view full EDI XML content!")
    else:
        print_error("SOME TESTS FAILED")
    
    print()
    print("="*80)
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
