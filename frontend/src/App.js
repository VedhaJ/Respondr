import React, { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import {
  ShieldCheck,
  Mail,
  Instagram,
  Facebook,
  MessageCircle,
  Twitter,
  CheckCircle2,
  AlertTriangle,
  Lock,
  ArrowLeft,
  ExternalLink,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Toaster, toast } from "sonner";

const API = "http://127.0.0.1:8000/api";

const iconMap = {
  Instagram: Instagram,
  Mail: Mail,
  Facebook: Facebook,
  MessageCircle: MessageCircle,
  Twitter: Twitter,
  ShieldCheck: ShieldCheck,
};

/* ===========================
   LANDING PAGE
=========================== */

const LandingPage = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      const response = await axios.get(`${API}/incidents`);
      setIncidents(response.data);
    } catch (error) {
      toast.error("Failed to load incident types");
    } finally {
      setLoading(false);
    }
  };

  const handleIncidentSelect = (incident) => {
    navigate(`/incident/${incident.platform}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <Toaster position="top-right" />

      <header className="bg-white border-b shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold">Respondr</h1>
        </div>
      </header>

      <section className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Get Help with Your <span className="text-primary">Compromised Account</span>
          </h2>
          <p className="text-slate-600">
            Step-by-step official recovery guidance for cyber incidents.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading ? (
            <div className="col-span-full text-center py-12">
              <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            incidents.map((incident) => {
              const IconComponent = iconMap[incident.icon] || ShieldCheck;
              return (
                <Card
                  key={incident.id}
                  className="p-6 cursor-pointer hover:shadow-md transition"
                  onClick={() => handleIncidentSelect(incident)}
                >
                  <IconComponent className="w-8 h-8 text-primary mb-4" />
                  <h3 className="text-xl font-semibold mb-2">{incident.title}</h3>
                  <p className="text-slate-600">{incident.description}</p>
                </Card>
              );
            })
          )}
        </div>

        <div className="mt-12 text-center">
          <Button onClick={() => navigate("/prevention")}>
            <Lock className="w-4 h-4 mr-2" />
            View Prevention Tips
          </Button>
        </div>
      </section>
    </div>
  );
};

/* ===========================
   INCIDENT PAGE
=========================== */

const IncidentResponsePage = () => {
  const { platform } = useParams();
  const navigate = useNavigate();

  const [recoveryLinks, setRecoveryLinks] = useState([]);
  const [navigationGuide, setNavigationGuide] = useState(null);

  useEffect(() => {
    fetchRecoveryLinks();
    fetchNavigationGuide();
  }, [platform]);

  const fetchRecoveryLinks = async () => {
    try {
      const response = await axios.get(`${API}/recovery-links/${platform}`);
      setRecoveryLinks(response.data);
    } catch (error) {
      console.error("Error fetching recovery links");
    }
  };

  const fetchNavigationGuide = async () => {
    try {
      const response = await axios.get(`${API}/navigation-guide/${platform}`);
      setNavigationGuide(response.data);
    } catch (error) {
      console.error("Error fetching navigation guide");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Toaster position="top-right" />

      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate("/")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="text-xl font-bold">{platform} Recovery</h1>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-12 space-y-10">

        {/* Navigation Guide */}
        {navigationGuide && (
          <Card className="p-8 bg-white shadow-sm">
            <h2 className="text-2xl font-semibold mb-4">Step-by-Step Guide</h2>

            <ol className="space-y-3 list-decimal list-inside text-slate-700">
              {navigationGuide.steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>

            <a
              href={navigationGuide.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center mt-6 text-primary font-medium"
            >
              Visit Official Website
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>

            <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <div className="flex gap-2 items-start">
                <AlertTriangle className="w-5 h-5 text-amber-600" />
                <p className="text-sm text-amber-800">
                  {navigationGuide.warning}
                </p>
              </div>
            </div>
          </Card>
        )}

        {/* Recovery Links */}
        <div>
          <h2 className="text-2xl font-semibold mb-6">Official Recovery Resources</h2>

          <div className="space-y-4">
            {recoveryLinks.map((link) => (
              <Card key={link.id} className="p-6 bg-white shadow-sm">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{link.title}</h3>
                    <p className="text-sm text-slate-600">{link.description}</p>
                  </div>

                  {link.verified && (
                    <Badge className="bg-emerald-100 text-emerald-800">
                      <CheckCircle2 className="w-3 h-3 mr-1" />
                      Verified
                    </Badge>
                  )}
                </div>

                <a
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-primary mt-3"
                >
                  Go to Official Support
                  <ExternalLink className="w-4 h-4 ml-2" />
                </a>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

/* ===========================
   PREVENTION PAGE
=========================== */
const PreventionPage = () => {
  const [tips, setTips] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API}/prevention-tips`)
      .then((res) => setTips(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate("/")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="text-xl font-bold">Prevention Tips</h1>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-12 space-y-6">
        {tips.map((tip) => (
          <Card key={tip.id} className="p-6 bg-white shadow-sm">
            
            {/* Platform Name */}
            <h3 className="text-xl font-semibold mb-4 capitalize">
              {tip.platform.replace(/-/g, " ")}
            </h3>

            {/* Tips List */}
            <ul className="list-disc list-inside space-y-2 text-slate-700">
              {tip.tips.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ul>

          </Card>
        ))}
      </section>
    </div>
  );
};

/* ===========================
   ROUTER
=========================== */

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/incident/:platform" element={<IncidentResponsePage />} />
        <Route path="/prevention" element={<PreventionPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;