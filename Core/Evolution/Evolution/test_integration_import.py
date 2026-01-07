try:
    from self_integration import ElysiaIntegrator
    print("✅ Import successful")
    integrator = ElysiaIntegrator()
    print("✅ Instantiation successful")
except Exception as e:
    print(f"❌ Error: {e}")
